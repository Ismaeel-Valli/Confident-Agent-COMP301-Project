import { rankFuzzyMatches } from '../filesystem/fuzzySearch';
import { text, type Tool, type LMStudioClient } from '@lmstudio/sdk';
import { z } from 'zod';
import { catalog } from '../catalog';
import { makeTool, validatePath, safeImplementation, type Context } from '../runtime';
import { join, resolve, dirname, relative, isAbsolute } from 'path';
import { rm, writeFile, readdir, readFile, stat, mkdir, rename, copyFile, appendFile } from 'fs/promises';
import type { Browser,Page } from 'puppeteer';
import { executeBrowserActions } from './browserActions';
import { performRagOnText } from './retrieval';
  const browserActionSchema = z.object({
    type: z.enum(["wait_for_selector", "wait", "click", "type", "press", "select", "hover", "scroll", "evaluate"]),
    selector: z.string().optional().describe("CSS selector used by selector-based actions."),
    text: z.string().optional().describe("Text payload for type action."),
    value: z.string().optional().describe("Value payload for select action."),
    key: z.string().optional().describe("Keyboard key for press action (e.g., Enter, Tab)."),
    milliseconds: z.number().int().min(0).max(30000).optional().describe("Delay in milliseconds for wait action."),
    x: z.number().optional().describe("Horizontal scroll delta for scroll action."),
    y: z.number().optional().describe("Vertical scroll delta for scroll action."),
    script: z.string().optional().describe("JavaScript snippet for evaluate action (executed in page context)."),
  });


let browserSession: {browser:Browser;page:Page;currentUrl:string}|null=null;
export function createWebTools(ctx:Context):Tool[]{
 const tool=makeTool(ctx),tools:Tool[]=[];
 const client=ctx.client, embeddingModelName=ctx.embeddingModel,allowBrowserControl=true,enableWikipedia=true;
const webSearchTool = tool({
    name: "web_search",
    description: catalog.web_search.description,
    parameters: {
      query: z.string(),
      providers: z.array(z.enum(["duckduckgo-api", "duckduckgo-fetch", "duckduckgo-html", "google", "bing"]))
        .optional()
        .describe("Optional: List of specific providers. If omitted, fallback chain is: DDG Fetch (no Chrome) -> DDG API -> DDG browser -> Google -> Bing."),
    },
    implementation: async ({ query, providers }) => {
      type SearchProvider = "duckduckgo-api" | "duckduckgo-fetch" | "duckduckgo-html" | "google" | "bing";
      type SearchResult = { title: string; link: string; snippet: string; provider: SearchProvider };

      const results: SearchResult[] = [];
      const errors: string[] = [];
      const logs: string[] = [];

      const decodeHtmlEntities = (value: string) =>
        value
          .replace(/&quot;/g, "\"")
          .replace(/&#39;/g, "'")
          .replace(/&apos;/g, "'")
          .replace(/&lt;/g, "<")
          .replace(/&gt;/g, ">")
          .replace(/&nbsp;/g, " ")
          .replace(/&amp;/g, "&");

      const stripHtml = (value: string) =>
        decodeHtmlEntities(value)
          .replace(/<[^>]+>/g, " ")
          .replace(/\s+/g, " ")
          .trim();

      const normalizeDuckDuckGoLink = (link: string): string => {
        const decoded = decodeHtmlEntities(link);
        const absolute = decoded.startsWith("//")
          ? `https:${decoded}`
          : decoded.startsWith("/")
            ? `https://duckduckgo.com${decoded}`
            : decoded;

        try {
          const parsed = new URL(absolute);
          const redirect = parsed.searchParams.get("uddg");
          if (redirect) {
            return decodeURIComponent(redirect);
          }
        } catch {
          // Return original normalized URL below.
        }

        return absolute;
      };

      const parseDuckDuckGoHtml = (html: string, provider: "duckduckgo-fetch" | "duckduckgo-html"): SearchResult[] => {
        const parsedResults: SearchResult[] = [];
        const titleRegex = /<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi;
        let match: RegExpExecArray | null;

        while ((match = titleRegex.exec(html)) !== null) {
          const link = normalizeDuckDuckGoLink(match[1]);
          const title = stripHtml(match[2]);
          const nearbyHtml = html.slice(match.index, Math.min(html.length, match.index + 1800));
          const snippetMatch = nearbyHtml.match(/class="result__snippet"[^>]*>([\s\S]*?)<\/(?:a|div)>/i);
          const snippet = snippetMatch ? stripHtml(snippetMatch[1]) : "";

          if (title && link) {
            parsedResults.push({ title, link, snippet, provider });
          }
          if (parsedResults.length >= 10) break;
        }

        return parsedResults;
      };

      let sharedBrowser: Browser | null = null;
      const getBrowser = async () => {
        if (!sharedBrowser) {
          const puppeteer = await import("puppeteer");
          sharedBrowser = await puppeteer.launch({
            headless: true,
            args: ["--no-sandbox", "--disable-setuid-sandbox"],
          });
        }
        return sharedBrowser;
      };

      const searchFunctions: Record<SearchProvider, (q: string) => Promise<SearchResult[]>> = {
        "duckduckgo-api": async (q: string) => {
          const { search, SafeSearchType } = await import("duck-duck-scrape");
          let attempt = 0;
          let lastError: unknown = null;

          while (attempt < 2) {
            try {
              const r = await search(q, { safeSearch: SafeSearchType.OFF });
              if (r.results && r.results.length > 0) {
                return r.results.slice(0, 10).map((result: any) => ({
                  title: result.title,
                  link: result.url,
                  snippet: result.description,
                  provider: "duckduckgo-api",
                }));
              }
              break;
            } catch (e) {
              lastError = e;
              attempt++;
              await new Promise(res => setTimeout(res, 1000));
            }
          }

          if (lastError) {
            throw lastError;
          }
          throw new Error("DuckDuckGo API returned no results");
        },

        "duckduckgo-fetch": async (q: string) => {
          const response = await fetch(`https://html.duckduckgo.com/html/?q=${encodeURIComponent(q)}`, {
            headers: {
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
              "Accept-Language": "en-US,en;q=0.9",
            },
          });
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
          }

          const html = await response.text();
          const extracted = parseDuckDuckGoHtml(html, "duckduckgo-fetch");
          if (extracted.length > 0) return extracted;
          throw new Error("No results parsed from DuckDuckGo HTML");
        },

        "duckduckgo-html": async (q: string) => {
          const browser = await getBrowser();
          try {
            const page = await browser.newPage();
            await page.goto(`https://html.duckduckgo.com/html/?q=${encodeURIComponent(q)}`, { waitUntil: "networkidle2", timeout: 15000 });

            const html = await page.content();
            const extracted = parseDuckDuckGoHtml(html, "duckduckgo-html");
            if (extracted.length > 0) return extracted;
            throw new Error("No results found");
          } finally {
            await browser.close();
            sharedBrowser = null;
          }
        },

        "google": async (q: string) => {
          const browser = await getBrowser();
          try {
            const page = await browser.newPage();
            await page.goto(`https://www.google.com/search?q=${encodeURIComponent(q)}`, { waitUntil: "networkidle2", timeout: 15000 });

            const extracted = await page.evaluate(() => {
              const items = document.querySelectorAll("div.g");
              const data = [];
              for (const item of items) {
                const titleEl = item.querySelector("h3");
                const linkEl = item.querySelector("a");
                const snippetEl = item.querySelector('div[style*="-webkit-line-clamp"]') || item.querySelector("div.VwiC3b");
                if (titleEl && linkEl) {
                  data.push({
                    title: titleEl.innerText,
                    link: linkEl.getAttribute("href") || "",
                    snippet: snippetEl ? (snippetEl as HTMLElement).innerText : "",
                    provider: "google" as const,
                  });
                }
              }
              return data;
            });
            if (extracted.length > 0) return extracted.slice(0, 10);
            throw new Error("No results found");
          } finally {
            await browser.close();
            sharedBrowser = null;
          }
        },

        "bing": async (q: string) => {
          const browser = await getBrowser();
          try {
            const page = await browser.newPage();
            await page.goto(`https://www.bing.com/search?q=${encodeURIComponent(q)}`, { waitUntil: "networkidle2", timeout: 15000 });

            const extracted = await page.evaluate(() => {
              const items = document.querySelectorAll("li.b_algo");
              const data = [];
              for (const item of items) {
                const titleEl = item.querySelector("h2 a");
                const linkEl = item.querySelector("h2 a");
                const snippetEl = item.querySelector("p");
                if (titleEl && linkEl) {
                  data.push({
                    title: (titleEl as HTMLElement).innerText,
                    link: linkEl.getAttribute("href") || "",
                    snippet: snippetEl ? (snippetEl as HTMLElement).innerText : "",
                    provider: "bing" as const,
                  });
                }
              }
              return data;
            });
            if (extracted.length > 0) return extracted.slice(0, 10);
            throw new Error("No results found");
          } finally {
            await browser.close();
            sharedBrowser = null;
          }
        },
      };

      if (providers && providers.length > 0) {
        for (const providerKey of providers) {
          try {
            logs.push(`[Manual] Attempting ${providerKey}...`);
            const pResults = await searchFunctions[providerKey](query);
            results.push(...pResults);
            logs.push(`[Manual] Success: ${providerKey} found ${pResults.length} results.`);
          } catch (e) {
            const errMsg = e instanceof Error ? e.message : String(e);
            errors.push(`${providerKey}: ${errMsg}`);
            logs.push(`[Manual] Failed: ${providerKey} - ${errMsg}`);
          }
        }
      } else {
        const chain: SearchProvider[] = ["duckduckgo-fetch", "duckduckgo-api", "duckduckgo-html", "google", "bing"];
        const browserProviders: SearchProvider[] = ["duckduckgo-html", "google", "bing"];
        let chromeUnavailable = false;

        for (let i = 0; i < chain.length; i++) {
          const providerKey = chain[i];
          if (chromeUnavailable && browserProviders.includes(providerKey)) {
            logs.push(`[Fallback Chain] Skipping ${providerKey}: Chrome not available on this system.`);
            continue;
          }
          const nextProvider = chain[i + 1];
          try {
            logs.push(`[Fallback Chain] Attempting ${providerKey}...`);
            const pResults = await searchFunctions[providerKey](query);
            results.push(...pResults);
            logs.push(`[Fallback Chain] Success: ${providerKey} found ${pResults.length} results. Stopping chain.`);
            break;
          } catch (e) {
            const errMsg = e instanceof Error ? e.message : String(e);
            errors.push(`${providerKey}: ${errMsg}`);
            if (/chrome|chromium/i.test(errMsg) && browserProviders.includes(providerKey)) {
              chromeUnavailable = true;
              logs.push(`[Fallback Chain] Failed: ${providerKey} - Chrome not available. Skipping all browser-based providers.`);
            } else {
              const nextMsg = nextProvider ? `Falling back to ${nextProvider}...` : "No more providers.";
              logs.push(`[Fallback Chain] Failed: ${providerKey} - ${errMsg}. ${nextMsg}`);
            }
          }
        }
      }

      if (results.length === 0) {
        return {
          error: "All attempted search providers failed.",
          attempts: errors,
          trace: logs,
        };
      }

      const seenLinks = new Set<string>();
      const dedupedResults = results.filter(r => {
        const key = r.link.trim();
        if (!key || seenLinks.has(key)) return false;
        seenLinks.add(key);
        return true;
      });

      return {
        results: dedupedResults,
        meta: {
          total_found: dedupedResults.length,
          providers_used: [...new Set(dedupedResults.map(r => r.provider))],
          no_api_key_required: true,
          trace: logs,
        },
      };
    },
  });
tools.push(webSearchTool);

const fetchWebContentTool = tool({
    name: "fetch_web_content",
    description: catalog.fetch_web_content.description,
    parameters: {
      url: z.string(),
    },
    implementation: async ({ url }) => {
      try {
        const response = await fetch(url, {signal:AbortSignal.timeout(20000)});
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        let text = await response.text();

        const result: any = {
          url,
          status: response.status,
        };

        const titleMatch = text.match(/<title[^>]*>([^<]+)<\/title>/i);
        if (titleMatch) result.title = titleMatch[1];

        const { compile } = await import("html-to-text");
        const compiledConvert = compile({
          wordwrap: false,
          selectors: [
            { selector: "a", options: { ignoreHref: true } },
            { selector: "img", format: "skip" },
          ],
        });

        text = compiledConvert(text);

        result.content = text.substring(0, 40000) + (text.length > 40000 ? "... (truncated)" : "");

        return result;
      } catch (error) {
        return {
          error: `Failed to fetch URL: ${error instanceof Error ? error.message : String(error)}`,
        };
      }
    },
  });
tools.push(fetchWebContentTool);

const ragWebContentTool = tool({
    name: "rag_web_content",
    description: catalog.rag_web_content.description,
    parameters: {
      url: z.string(),
      query: z.string(),
    },
    implementation: async ({ url, query }) => {
      try {
        // 1. Fetch content
        const response = await fetch(url, {signal:AbortSignal.timeout(20000)});
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        let text = await response.text();

        const { compile } = await import("html-to-text");
        const compiledConvert = compile({
          wordwrap: false,
          selectors: [
            { selector: "a", options: { ignoreHref: true } },
            { selector: "img", format: "skip" },
          ],
        });

        text = compiledConvert(text);

        if (text.length === 0) {
          return { error: "Could not extract any text from the URL." };
        }

        // 3. Perform RAG
        if (!client) {
          return { error: "LM Studio Client is not available. RAG features require the client to be initialized." };
        }
        const ragResults = await performRagOnText(text, query, client, embeddingModelName);

        return {
          url: url,
          query: query,
          relevant_chunks: ragResults,
        };

      } catch (error) {
        return { error: `Failed during RAG web search: ${error instanceof Error ? error.message : String(error)}` };
      }
    },
  });
tools.push(ragWebContentTool);

const wikipediaSearchTool = tool({
    name: "wikipedia_search",
    description: catalog.wikipedia_search.description,
    parameters: {
      query: z.string(),
      lang: z.string().optional().describe("Language code (default: en)"),
    },
    implementation: safeImplementation(
      async ({ query, lang = "en" }) => {
        try {
          const searchUrl = `https://${lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&format=json`;
          const searchResponse = await fetch(searchUrl);
          const searchData = await searchResponse.json();

          if (!searchData.query || !searchData.query.search || searchData.query.search.length === 0) {
            return { results: "No Wikipedia articles found." };
          }

          const results = [];
          for (const item of searchData.query.search.slice(0, 3)) { // Top 3
            const pageUrl = `https://${lang}.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&pageids=${item.pageid}&format=json`;
            const pageResponse = await fetch(pageUrl);
            const pageData = await pageResponse.json();
            const page = pageData.query.pages[item.pageid];

            results.push({
              title: item.title,
              summary: page.extract.substring(0, 2000) + (page.extract.length > 2000 ? "..." : ""),
              url: `https://${lang}.wikipedia.org/wiki/${encodeURIComponent(item.title.replace(/ /g, "_"))}`
            });
          }
          return { results };
        } catch (error) {
          return { error: `Wikipedia search failed: ${error instanceof Error ? error.message : String(error)}` };
        }
      },
      enableWikipedia,
      "wikipedia_search"
    )
  });
tools.push(wikipediaSearchTool);

const browserSessionOpenTool = tool({
    name: "browser_session_open",
    description: catalog.browser_session_open.description,
    parameters: {
      url: z.string(),
      wait_for_selector: z.string().optional().describe("Optional selector to wait for after navigation."),
      include_page_text: z.boolean().optional().describe("If true (default), returns full page text content after opening."),
    },
    implementation: safeImplementation(async ({ url, wait_for_selector, include_page_text = true }) => {
      try {
        if (browserSession) {
          await browserSession.browser.close().catch(() => { });
          browserSession = null;
        }

        const puppeteer = await import("puppeteer");
        const browser = await puppeteer.launch({
          headless: true,
          args: ["--no-sandbox", "--disable-setuid-sandbox"],
        });
        const page = await browser.newPage();
        await page.goto(url, { waitUntil: "networkidle0", timeout: 30000 });
        if (wait_for_selector) {
          await page.waitForSelector(wait_for_selector, { timeout: 15000 });
        }

        browserSession = {
          browser,
          page,
          currentUrl: page.url(),
        };

        const pageText = include_page_text
          ? await page.evaluate(() => document.body.innerText || "")
          : undefined;

        return {
          success: true,
          session_active: true,
          url: page.url(),
          title: await page.title(),
          text_content: pageText,
          text_length: pageText ? pageText.length : 0,
          message: "Browser session opened.",
        };
      } catch (error) {
        return { error: `Failed to open browser session: ${error instanceof Error ? error.message : String(error)}` };
      }
    }, allowBrowserControl, "browser_control"),
  });
tools.push(browserSessionOpenTool);

const browserSessionControlTool = tool({
    name: "browser_session_control",
    description: catalog.browser_session_control.description,
    parameters: {
      actions: z.array(browserActionSchema).optional().describe("Optional scripted browser actions to execute on the active page."),
      read_page: z.boolean().optional().describe("If true (default), returns page metadata. Full text is returned only on URL change or when full_read=true."),
      full_read: z.boolean().optional().describe("If true, forces full page text output even when URL has not changed."),
      screenshot_path: z.string().optional().describe("Optional screenshot output path."),
      full_page_screenshot: z.boolean().optional().describe("If true, captures full page screenshot."),
      fuzzy_find: z.string().optional().describe("Optional fuzzy-find query for in-page content/selectors."),
      max_results: z.number().int().min(1).max(20).optional().describe("Max fuzzy results to return (default: 5)."),
    },
    implementation: safeImplementation(async ({ actions, read_page = true, full_read = false, screenshot_path, full_page_screenshot, fuzzy_find, max_results = 5 }) => {
      if (!browserSession) {
        return { error: "No active browser session. Call 'browser_session_open' first." };
      }

      try {
        const beforeUrl = browserSession.page.url();
        const actionLog = await executeBrowserActions(browserSession.page, actions || []);
        const afterUrl = browserSession.page.url();
        const urlChanged = beforeUrl !== afterUrl;
        browserSession.currentUrl = afterUrl;

        let screenshotSaved = false;
        if (screenshot_path) {
          const screenshotFilePath = validatePath(ctx.cwd, screenshot_path);
          await browserSession.page.screenshot({ path: screenshotFilePath, fullPage: full_page_screenshot ?? false });
          screenshotSaved = true;
        }

        let pageSnapshot:
          | { url: string; title: string; text_content?: string; text_length?: number; note?: string }
          | undefined = undefined;
        if (read_page) {
          const title = await browserSession.page.title();
          if (urlChanged || full_read) {
            const textContent = await browserSession.page.evaluate(() => document.body.innerText || "");
            pageSnapshot = {
              url: afterUrl,
              title,
              text_content: textContent,
              text_length: textContent.length,
            };
          } else {
            pageSnapshot = {
              url: afterUrl,
              title,
              note: "Full page text omitted (URL unchanged). Set full_read=true to force full output.",
            };
          }
        }

        let fuzzyResults: Array<{ text: string; selector: string; score: number }> = [];
        if (typeof fuzzy_find === "string" && fuzzy_find.trim()) {
          const candidates = await browserSession.page.evaluate(() => {
            const dedup = new Map<string, { text: string; selector: string }>();
            const nodes = document.querySelectorAll("a,button,input,textarea,select,[role='button'],[aria-label],h1,h2,h3,h4,h5,h6,p,span");

            const clean = (value: string) => value.replace(/\s+/g, " ").trim();
            const classSelector = (el: Element) => {
              const classes = Array.from(el.classList).slice(0, 2).map(c => c.replace(/[^a-zA-Z0-9_-]/g, ""));
              return classes.length > 0 ? `.${classes.join(".")}` : "";
            };

            const buildSelector = (el: Element) => {
              if ((el as HTMLElement).id) return `#${(el as HTMLElement).id}`;
              const name = el.getAttribute("name");
              if (name) return `${el.tagName.toLowerCase()}[name="${name.replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"]`;
              return `${el.tagName.toLowerCase()}${classSelector(el)}`;
            };

            for (const node of nodes) {
              const element = node as HTMLElement;
              const text = clean(
                element.innerText ||
                (element as HTMLInputElement).value ||
                element.getAttribute("aria-label") ||
                "",
              );
              if (!text) continue;
              const selector = buildSelector(element);
              const key = `${text}||${selector}`;
              if (!dedup.has(key)) {
                dedup.set(key, { text: text.substring(0, 200), selector });
              }
              if (dedup.size >= 400) break;
            }

            return Array.from(dedup.values());
          });

          const ranked = candidates
            .map(candidate => ({
              ...candidate,
              score: Math.max(
                rankFuzzyMatches(fuzzy_find, [candidate.text], 1)[0]?.score ?? 0,
                rankFuzzyMatches(fuzzy_find, [candidate.selector], 1)[0]?.score ?? 0,
              ),
            }))
            .sort((a, b) => b.score - a.score)
            .slice(0, max_results);

          fuzzyResults = ranked.map(item => ({
            text: item.text,
            selector: item.selector,
            score: item.score,
          }));
        }

        return {
          success: true,
          session_active: true,
          actions_executed: actionLog,
          screenshot_saved: screenshotSaved,
          url_changed: urlChanged,
          url_change_notice: urlChanged ? `Url changed to -> [${afterUrl}]` : undefined,
          page: pageSnapshot,
          fuzzy_find_results: fuzzyResults,
        };
      } catch (error) {
        return { error: `Browser session control failed: ${error instanceof Error ? error.message : String(error)}` };
      }
    }, allowBrowserControl, "browser_control"),
  });
tools.push(browserSessionControlTool);

const browserSessionCloseTool = tool({
    name: "browser_session_close",
    description: catalog.browser_session_close.description,
    parameters: {},
    implementation: safeImplementation(async () => {
      if (!browserSession) {
        return { success: true, session_active: false, message: "No active browser session." };
      }

      try {
        await browserSession.browser.close();
        browserSession = null;
        return { success: true, session_active: false, message: "Browser session closed." };
      } catch (error) {
        return { error: `Failed to close browser session: ${error instanceof Error ? error.message : String(error)}` };
      }
    }, allowBrowserControl, "browser_control"),
  });
tools.push(browserSessionCloseTool);

const browserOpenPageTool = tool({
    name: "browser_open_page",
    description: catalog.browser_open_page.description,
    parameters: {
      url: z.string(),
      screenshot_path: z.string().optional().describe("Path to save a screenshot (e.g., 'screenshot.png')."),
      wait_for_selector: z.string().optional().describe("CSS selector to wait for before returning."),
      full_page_screenshot: z.boolean().optional().describe("If true, captures the full page when taking a screenshot."),
      actions: z.array(browserActionSchema).optional().describe("Optional scripted browser steps to run after navigation."),
    },
    implementation: safeImplementation(async ({ url, screenshot_path, wait_for_selector, full_page_screenshot, actions }) => {
      let browser;
      try {
        // Dynamically import puppeteer
        const puppeteer = await import("puppeteer");
        browser = await puppeteer.launch({
          headless: true,
          args: ["--no-sandbox", "--disable-setuid-sandbox"],
        });
        const page = await browser.newPage();

        try {
          await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

          if (wait_for_selector) {
            await page.waitForSelector(wait_for_selector, { timeout: 10000 });
          }

          const beforeActionUrl = page.url();
          const action_log = await executeBrowserActions(page, actions || []);
          const currentUrl = page.url();
          const urlChanged = currentUrl !== beforeActionUrl;

          const title = await page.title();
          const textContent = await page.evaluate(() => document.body.innerText || "");

          let screenshot_saved = false;
          if (screenshot_path) {
            const screenshotFilePath = validatePath(ctx.cwd, screenshot_path);
            await page.screenshot({ path: screenshotFilePath, fullPage: full_page_screenshot ?? false });
            screenshot_saved = true;
          }

          return {
            url: currentUrl,
            title,
            text_content: textContent.substring(0, 5000),
            screenshot_saved,
            actions_executed: action_log,
            url_changed: urlChanged,
            url_change_notice: urlChanged ? `Url changed to -> [${currentUrl}]` : undefined,
          };
        } finally {
          await browser.close();
        }
      } catch (error) {
        if (browser) {
          await browser.close().catch(() => { });
        }
        return { error: `Browser operation failed: ${error instanceof Error ? error.message : String(error)}` };
      }
    }, allowBrowserControl, "browser_control")
  });
tools.push(browserOpenPageTool);
return tools;
}

import { text, type Tool, type LMStudioClient } from '@lmstudio/sdk';
import { z } from 'zod';
import { catalog } from '../catalog';
import { makeTool, validatePath, safeImplementation, type Context } from '../runtime';
import { join, resolve, dirname, relative, isAbsolute } from 'path';
import { rm, writeFile, readdir, readFile, stat, mkdir, rename, copyFile, appendFile, lstat } from 'fs/promises';
import { rankFuzzyMatches } from './fuzzySearch';
import { cosineSimilarity } from '../web/retrieval';
export function createFilesystemTools(ctx:Context):Tool[]{
 const tool=makeTool(ctx),tools:Tool[]=[];
 const client=ctx.client, embeddingModelName=ctx.embeddingModel,enableLocalRag=ctx.enabled('rag_local_files');
const readDocumentTool = tool({
    name: "read_document",
    description: catalog.read_document.description,
    parameters: {
      file_path: z.string(),
    },
    implementation: async ({ file_path }) => {
      const fpath = validatePath(ctx.cwd, file_path);
      const ext = fpath.split('.').pop()?.toLowerCase();

      try {
        if (ext === 'pdf') {
          // Polyfill DOMMatrix for pdf-parse v2 (required for node environment)
          if (typeof global.DOMMatrix === 'undefined') {
            (global as any).DOMMatrix = class DOMMatrix {
              constructor(arg?: any) {
                (this as any).a = 1; (this as any).b = 0; (this as any).c = 0; (this as any).d = 1; (this as any).e = 0; (this as any).f = 0;
                if (Array.isArray(arg)) {
                  (this as any).a = arg[0]; (this as any).b = arg[1];
                  (this as any).c = arg[2]; (this as any).d = arg[3];
                  (this as any).e = arg[4]; (this as any).f = arg[5];
                }
              }
            };
          }

          // Dynamically require pdf-parse v2 class
          const { PDFParse } = require("pdf-parse");

          const dataBuffer = await readFile(fpath);
          // Use new class-based API
          const parser = new PDFParse({ data: dataBuffer });
          const textResult = await parser.getText();
          const infoResult = await parser.getInfo(); // Optional: get metadata

          await parser.destroy(); // Cleanup

          return { content: textResult.text, metadata: infoResult.info };
        } else if (ext === 'docx') {
          const mammoth = await import("mammoth");
          const result = await mammoth.extractRawText({ path: fpath });
          return { content: result.value, messages: result.messages };
        } else {
          return { error: "Unsupported document format. Use read_file for text files." };
        }
      } catch (e) {
        return { error: `Failed to read document: ${e instanceof Error ? e.message : String(e)}` };
      }
    }
  });
tools.push(readDocumentTool);

const saveFileTool = tool({
    name: "save_file",
    description: catalog.save_file.description,
    parameters: {
      file_name: z.string().optional(),
      content: z.string().optional(),
      files: z.array(z.object({ file_name: z.string(), content: z.string() })).optional().describe("For saving multiple files at once. E.g. [{file_name: 'a.txt', content: 'hello'}]"),
    },
    implementation: async ({ file_name, content, files }) => {

      const filesToSave = Array.isArray(files) ? files : [];
      if (file_name && content) {
        filesToSave.push({ file_name, content });
      }

      if (filesToSave.length === 0) {
        return { error: "Must provide either file_name and content, or a files array." };
      }

      const savedPaths: string[] = [];
      const errors: string[] = [];

      for (const file of filesToSave) {

      // Validate filename
      if (!file.file_name || file.file_name.trim().length === 0) {
        errors.push(`Filename cannot be empty`);
        continue;
      }

      if (file.file_name && /[ \*\?<>|"]/.test(file.file_name)) {
        errors.push("Filename " + file.file_name + " contains invalid characters");
      }

        try {
          const filePath = validatePath(ctx.cwd, file.file_name);
          await mkdir(dirname(filePath), { recursive: true });
          await writeFile(filePath, file.content, "utf-8");
          savedPaths.push(filePath);
        } catch (e) {
          errors.push(`Failed to save ${file.file_name}: ${e instanceof Error ? e.message : String(e)}`);
        }
      }

      if (errors.length > 0 && savedPaths.length === 0) {
        return { error: errors.join("\n") };
      }

      return {
        success: true,
        paths: savedPaths,
        errors: errors.length > 0 ? errors : undefined,
      };
    },
  });
tools.push(saveFileTool);

const replaceTextTool = tool({
    name: "replace_text_in_file",
    description: catalog.replace_text_in_file.description,
    parameters: {
      file_name: z.string(),
      old_string: z.string().describe("The exact text to replace. Must be unique in the file."),
      new_string: z.string().describe("The text to insert in place of old_string."),
    },
    implementation: async ({ file_name, old_string, new_string }) => {
      try {

        if (!old_string || old_string.length === 0) {
          return { error: "old_string cannot be empty" };
        }

        const filePath = validatePath(ctx.cwd, file_name);
        const content = await readFile(filePath, "utf-8");

        if (!content.includes(old_string)) {
          return { error: "Could not find the exact 'old_string' in the file. Please check whitespace and indentation." };
        }

        const occurrenceCount = content.split(old_string).length - 1;
        if (occurrenceCount > 1) {
          return { error: `Found ${occurrenceCount} occurrences of 'old_string'. Please provide more context (surrounding lines) in 'old_string' to make it unique.` };
        }

        const newContent = content.replace(old_string, new_string);
        await writeFile(filePath, newContent, "utf-8");

        return { success: true, message: `Successfully replaced text in ${file_name}` };
      } catch (e) {
        return { error: `Failed to replace text: ${e instanceof Error ? e.message : String(e)}` };
      }
    },
  });
tools.push(replaceTextTool);

const multiReplaceTextTool = tool({
    name: "multi_replace_text",
    description: catalog.multi_replace_text.description,
    parameters: {
      file_name: z.string(),
      replacements: z.array(z.object({
        start_line: z.number().int().min(1),
        end_line: z.number().int().min(1),
        old_string: z.string(),
        new_string: z.string()
      })).describe("Array of replacements to make in the file")
    },
    implementation: async ({ file_name, replacements }) => {
      try {
        const filePath = validatePath(ctx.cwd, file_name);
        const content = await readFile(filePath, "utf-8");
        let lines = content.split("\n");
        let errors = [];
        
        // Sort replacements from bottom to top to avoid line index shifts!
        const sortedReplacements = [...replacements].sort((a, b) => b.start_line - a.start_line);
        
        for (const rep of sortedReplacements) {
          if (rep.start_line > rep.end_line) {
            errors.push(`Invalid range: start_line ${rep.start_line} > end_line ${rep.end_line}`);
            continue;
          }
          const chunk = lines.slice(rep.start_line - 1, rep.end_line).join("\n");
          if (!chunk.includes(rep.old_string)) {
            errors.push(`Could not find old_string between lines ${rep.start_line}-${rep.end_line}`);
            continue;
          }
          // Only replace the first occurrence in the exact block
          const newChunk = chunk.replace(rep.old_string, rep.new_string);
          const newChunkLines = newChunk.split("\n");
          
          lines.splice(rep.start_line - 1, rep.end_line - rep.start_line + 1, ...newChunkLines);
        }
        
        if (errors.length > 0) {
          return { error: "Replacements failed:\n" + errors.join("\n") };
        }
        
        await writeFile(filePath, lines.join("\n"), "utf-8");
        return { success: true, message: `Applied ${replacements.length} replacements to ${file_name}` };
      } catch (e) {
        return { error: `Failed to multi-replace: ${e instanceof Error ? e.message : String(e)}` };
      }
    }
  });
tools.push(multiReplaceTextTool);

const searchDirectoryTool = tool({
    name: "search_directory",
    description: catalog.search_directory.description,
    parameters: {
      directory_path: z.string().optional().describe("Directory to search. Defaults to workspace root."),
      pattern: z.string().describe("Regex pattern or string to search for"),
      use_regex: z.boolean().optional().default(false)
    },
    implementation: async ({ directory_path, pattern, use_regex }) => {
      try {
        const targetDir = directory_path ? validatePath(ctx.cwd, directory_path) : ctx.cwd;
        const regex = new RegExp(use_regex ? pattern : pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
        const results: string[] = [];
        let searchedCount = 0;
        
        async function search(dir: string) {
          const files = await readdir(dir);
          for (const file of files) {
            if (file === "node_modules" || file === ".git" || file.startsWith(".")) continue;
            const fullPath = join(dir, file);
            const st = await lstat(fullPath);
            if(st.isSymbolicLink()) continue;
            if (st.isDirectory()) {
              await search(fullPath);
            } else if (st.isFile()) {
              if (st.size > 2000000) continue; // Skip large files > 2MB
              try {
                const content = await readFile(fullPath, "utf-8");
                if (content.includes('\0')) continue; // Skip binary
                
                const lines = content.split('\n');
                for (let i = 0; i < lines.length; i++) {
                  if (lines[i].match(regex)) {
                    results.push(`${relative(ctx.cwd, fullPath)}:${i+1} => ${lines[i].trim()}`);
                    if (results.length >= 100) return; // Limit output
                  }
                }
                searchedCount++;
              } catch (e) {}
            }
          }
        }
        
        await search(targetDir);
        
        if (results.length === 0) return { message: `No matches found. Searched ${searchedCount} files.` };
        return { matches: results, message: `Found ${results.length} matches across ${searchedCount} files searched.` };
      } catch (e) {
        return { error: `Search failed: ${e instanceof Error ? e.message : String(e)}` };
      }
    }
  });
tools.push(searchDirectoryTool);

const listDirectoryTool = tool({
    name: "list_directory",
    description: catalog.list_directory.description,
    parameters: {
      path: z.string().optional().describe("The path to the directory to list. Defaults to current working directory."),
    },
    implementation: async ({ path }) => {
      const targetPath = path ? validatePath(ctx.cwd, path) : ctx.cwd;
      const files = await readdir(targetPath);
      return {
        files,
      };
    },
  });
tools.push(listDirectoryTool);

const readFileTool = tool({
    name: "read_file",
    description: catalog.read_file.description,
    parameters: {
      file_name: z.string(),
    },
    implementation: async ({ file_name }) => {
      const filePath = validatePath(ctx.cwd, file_name);

      const stats = await stat(filePath);
      if (stats.size > 10_000_000) {
        return { error: "File too large (>10MB)" };
      }

      // Check for binary content (simple null byte check in first 1KB)
      // Read as buffer first
      const buffer = await readFile(filePath);
      // Check first 1024 bytes for null byte
      const checkBuffer = buffer.subarray(0, Math.min(buffer.length, 1024));
      if (checkBuffer.includes(0)) {
        return { error: "File appears to be binary and cannot be read as text." };
      }

      const content = buffer.toString("utf-8");
      return {
        content,
      };
    },
  });
tools.push(readFileTool);

const makeDirectoryTool = tool({
    name: "make_directory",
    description: catalog.make_directory.description,
    parameters: {
      directory_name: z.string(),
    },
    implementation: async ({ directory_name }) => {
      const dirPath = validatePath(ctx.cwd, directory_name);
      await mkdir(dirPath, { recursive: true });
      return {
        success: true,
        path: dirPath,
      };
    },
  });
tools.push(makeDirectoryTool);

const deletePathTool = tool({
    name: "delete_path",
    description: catalog.delete_path.description,
    parameters: {
      path: z.string(),
    },
    implementation: async ({ path }) => {
      const targetPath = validatePath(ctx.cwd, path);
      await rm(targetPath, { recursive: true, force: true });
      return {
        success: true,
        path: targetPath,
      };
    },
  });
tools.push(deletePathTool);

const deleteFilesByPatternTool = tool({
    name: "delete_files_by_pattern",
    description: catalog.delete_files_by_pattern.description,
    parameters: {
      pattern: z.string().describe("Regex pattern to match filenames (e.g., '^auto_gen_.*\\.txt$')"),
    },
    implementation: async ({ pattern }) => {
      try {

        // Validate regex complexity to prevent ReDoS
        if (pattern.length > 100) {
          return { error: "Pattern too complex (max 100 characters)" };
        }

        const regex = new RegExp(pattern);

        // Safety check for ReDoS
        const start = Date.now();
        regex.test("safe_test_string_for_redos_check_1234567890_safe_test_string_for_redos_check_1234567890");
        if (Date.now() - start > 100) {
          return { error: "Pattern is too complex or slow (ReDoS protection)." };
        }

        const files = await readdir(ctx.cwd);
        const deleted = [];

        for (const file of files) {
          if (regex.test(file)) {
            await rm(join(ctx.cwd, file), { force: true });
            deleted.push(file);
          }
        }
        return { deleted_count: deleted.length, deleted_files: deleted };
      } catch (e) {
        return { error: `Failed to delete files: ${e instanceof Error ? e.message : String(e)}` };
      }
    },
  });
tools.push(deleteFilesByPatternTool);

const moveFileTool = tool({
    name: "move_file",
    description: catalog.move_file.description,
    parameters: {
      source: z.string(),
      destination: z.string(),
    },
    implementation: async ({ source, destination }) => {
      const sourcePath = validatePath(ctx.cwd, source);
      const destPath = validatePath(ctx.cwd, destination);
      await rename(sourcePath, destPath);
      return {
        success: true,
        from: sourcePath,
        to: destPath,
      };
    },
  });
tools.push(moveFileTool);

const copyFileTool = tool({
    name: "copy_file",
    description: catalog.copy_file.description,
    parameters: {
      source: z.string(),
      destination: z.string(),
    },
    implementation: async ({ source, destination }) => {
      const sourcePath = validatePath(ctx.cwd, source);
      const destPath = validatePath(ctx.cwd, destination);
      await copyFile(sourcePath, destPath);
      return {
        success: true,
        from: sourcePath,
        to: destPath,
      };
    },
  });
tools.push(copyFileTool);

const findFilesTool = tool({
    name: "find_files",
    description: catalog.find_files.description,
    parameters: {
      pattern: z.string().describe("Substring to match in filename (case-insensitive)"),
      max_depth: z.number().optional().describe("Maximum depth to search (default: 5)"),
    },
    implementation: async ({ pattern, max_depth }) => {
      const depthLimit = max_depth ?? 5;
      const foundFiles: string[] = [];
      const lowerPattern = pattern.toLowerCase();

      async function scan(dir: string, currentDepth: number) {
        if (currentDepth > depthLimit) return;
        try {
          const entries = await readdir(dir, { withFileTypes: true });
          for (const entry of entries) {
            if (['node_modules', '.git', 'dist', '.lmstudio'].includes(entry.name)) continue;
            const fullPath = join(dir, entry.name);
            if (entry.isDirectory()) {
              await scan(fullPath, currentDepth + 1);
            } else if (entry.isFile()) {
              if (entry.name.toLowerCase().includes(lowerPattern)) {
                foundFiles.push(fullPath);
              }
            }
          }
        } catch (e) {
          // Ignore access errors
        }
      }

      await scan(ctx.cwd, 0);
      return {
        found_files: foundFiles.slice(0, 100), // Limit results
        count: foundFiles.length,
      };
    },
  });
tools.push(findFilesTool);

const fuzzyFindLocalFilesTool = tool({
    name: "fuzzy_find_local_files",
    description: catalog.fuzzy_find_local_files.description,
    parameters: {
      query: z.string().describe("Search query to match against file names/paths."),
      path: z.string().optional().describe("Sub-directory to search in (default: current directory)."),
      max_results: z.number().int().min(1).max(20).optional().describe("Max results to return (default: 5)."),
    },
    implementation: async ({ query, path = ".", max_results = 5 }) => {
      try {
        const targetDir = validatePath(ctx.cwd, path);
        const entries = await readdir(targetDir, { recursive: true, withFileTypes: true });
        const files = entries
          .filter(entry => entry.isFile())
          .map(entry => {
            const fullPath = join(entry.parentPath, entry.name);
            const relativePath = relative(targetDir, fullPath);
            return relativePath.replace(/\\/g, "/");
          });

        const ranked = rankFuzzyMatches(query, files, max_results);
        return {
          query,
          path: targetDir,
          results: ranked.map(item => ({
            path: item.value,
            score: item.score,
          })),
        };
      } catch (error) {
        return { error: `Fuzzy file search failed: ${error instanceof Error ? error.message : String(error)}` };
      }
    },
  });
tools.push(fuzzyFindLocalFilesTool);

const getFileMetadataTool = tool({
    name: "get_file_metadata",
    description: catalog.get_file_metadata.description,
    parameters: {
      path: z.string(),
    },
    implementation: async ({ path }) => {
      try {
        const targetPath = validatePath(ctx.cwd, path);
        const stats = await stat(targetPath);
        return {
          path: targetPath,
          size: stats.size,
          created: stats.birthtime,
          modified: stats.mtime,
          is_directory: stats.isDirectory(),
          is_file: stats.isFile(),
        };
      } catch (error) {
        return { error: `Failed to get metadata: ${error instanceof Error ? error.message : String(error)}` };
      }
    },
  });
tools.push(getFileMetadataTool);

const openFileTool = tool({
    name: "open_file",
    description: catalog.open_file.description,
    parameters: {
      target: z.string().describe("File path or URL"),
    },
    implementation: async ({ target }) => {
      // Resolve path if it's a file and not a URL
      let targetToOpen = target;
      if (!target.startsWith("http://") && !target.startsWith("https://")) {
        targetToOpen = validatePath(ctx.cwd, target);
      }

      const open = (await import("open")).default;
      await open(targetToOpen);

      return { success: true, message: `Opened ${targetToOpen}` };
    }
  });
tools.push(openFileTool);

const previewHtmlTool = tool({
    name: "preview_html",
    description: catalog.preview_html.description,
    parameters: {
      html_content: z.string(),
      file_name: z.string().optional().describe("Optional filename (default: preview.html)")
    },
    implementation: async ({ html_content, file_name }) => {
      const name = file_name || `preview_${Date.now()}.html`;
      const filePath = validatePath(ctx.cwd, name);
      await writeFile(filePath, html_content, "utf-8");

      // Open it
      const open = (await import("open")).default;
      await open(filePath);

      return { success: true, path: filePath, message: "HTML preview launched in browser." };
    }
  });
tools.push(previewHtmlTool);

const ragLocalFilesTool = tool({
    name: "rag_local_files",
    description: catalog.rag_local_files.description,
    parameters: {
      query: z.string(),
      path: z.string().optional().describe("Sub-directory to limit search (default: current working directory)"),
      file_pattern: z.string().optional().describe("File pattern to include (e.g. '.ts', 'src/'). Default: all text files."),
    },
    implementation: safeImplementation(
      async ({ query, path = ".", file_pattern = "" }) => {
        try {
          if (!client) return { error: "LM Studio Client unavailable." };

          const targetDir = validatePath(ctx.cwd, path);
          const entries = await readdir(targetDir, { recursive: true, withFileTypes: true });
          const textFiles = entries.filter(e => e.isFile() && !e.name.match(/\.(png|jpg|jpeg|gif|ico|exe|dll|bin)$/i));

          // Filter by pattern if provided
          const filteredFiles = file_pattern
            ? textFiles.filter(e => e.name.includes(file_pattern) || join(e.parentPath, e.name).includes(file_pattern))
            : textFiles;

          // Limit to avoid massive reads. 
          // In a real 'Gemini Flow' robust implementation, we'd use an index. 
          // Here we'll read top 50 files max to be safe.
          const filesToScan = filteredFiles.slice(0, 50);

          let allChunks: { chunk: string, score: number, file: string }[] = [];
          const embeddingModel = await client.embedding.model(embeddingModelName);
          const [queryEmbedding] = await embeddingModel.embed([query]);

          for (const file of filesToScan) {
            try {
              const fullPath = join(file.parentPath, file.name);
              const content = await readFile(fullPath, "utf-8");
              // reuse chunking logic
              const chunks = content.split(/\n\s*\n/).filter(c => c.trim().length > 20);
              if (chunks.length === 0) continue;

              // Batch embed chunks for this file
              const chunkEmbeddings = await embeddingModel.embed(chunks);

              chunks.forEach((chunk, i) => {
                const score = cosineSimilarity(queryEmbedding.embedding, chunkEmbeddings[i].embedding);
                if (score > 0.4) { // Threshold
                  allChunks.push({ chunk, score, file: file.name });
                }
              });

            } catch (e) {
              // ignore read errors
            }
          }

          // Sort all chunks
          allChunks.sort((a, b) => b.score - a.score);

          return {
            query,
            results: allChunks.slice(0, 10).map(c => ({
              file: c.file,
              score: c.score.toFixed(3),
              content: c.chunk
            }))
          };

        } catch (error) {
          return { error: `Local RAG failed: ${error instanceof Error ? error.message : String(error)}` };
        }
      },
      enableLocalRag,
      "rag_local_files"
    )
  });
tools.push(ragLocalFilesTool);

const insertAtLineTool = tool({
    name: "insert_at_line",
    description: catalog.insert_at_line.description,
    parameters: {
      file_name: z.string(),
      line_number: z.number().int().min(1).describe("The line number to insert at (1-indexed)"),
      content_to_insert: z.string().describe("The text content to insert at the specified line"),
    },
    implementation: async ({ file_name, line_number, content_to_insert }) => {
      try {
        const filePath = validatePath(ctx.cwd, file_name);
        let content = "";
        try {
          content = await readFile(filePath, "utf-8");
        } catch {
          if (line_number !== 1) {
            return { error: `File '${file_name}' does not exist. Can only insert at line 1 in a new file.` };
          }
        }
        
        const lines = content.split("\n");
        const insertIndex = Math.min(line_number - 1, lines.length);
        lines.splice(insertIndex, 0, content_to_insert);
        
        await writeFile(filePath, lines.join("\n"), "utf-8");
        return { 
          success: true, 
          message: `Inserted ${content_to_insert.split('\n').length} line(s) at line ${line_number} in ${file_name}`,
          new_line_count: lines.length 
        };
      } catch (e) {
        return { error: `Failed to insert text: ${e instanceof Error ? e.message : String(e)}` };
      }
    },
  });
tools.push(insertAtLineTool);

const appendFileTool = tool({
    name: "append_file",
    description: catalog.append_file.description,
    parameters: {
      file_name: z.string(),
      content: z.string().describe("The text content to append to the file"),
    },
    implementation: async ({ file_name, content }) => {
      try {
        const filePath = validatePath(ctx.cwd, file_name);
        await mkdir(dirname(filePath), { recursive: true });
        await appendFile(filePath, content, "utf-8");
        return { 
          success: true, 
          message: `Content appended to ${file_name}` 
        };
      } catch (e) {
        return { error: `Failed to append to file: ${e instanceof Error ? e.message : String(e)}` };
      }
    },
  });
tools.push(appendFileTool);

const readFileRangeTool = tool({
    name: "read_file_range",
    description: catalog.read_file_range.description,
    parameters: {
      file_name: z.string(),
      start_line: z.number().int().min(1).describe("Starting line number (1-indexed)"),
      end_line: z.number().int().min(1).describe("Ending line number (1-indexed, inclusive)"),
    },
    implementation: async ({ file_name, start_line, end_line }) => {
      try {
        const filePath = validatePath(ctx.cwd, file_name);
        const content = await readFile(filePath, "utf-8");
        const lines = content.split("\n");
        
        if (start_line > lines.length) {
          return { error: `Start line ${start_line} is beyond the end of the file (${lines.length} lines)` };
        }
        
        const actualEndLine = Math.min(end_line, lines.length);
        const selectedLines = lines.slice(start_line - 1, actualEndLine);
        
        const numberedContent = selectedLines.map((line, idx) => 
          `${start_line + idx}: ${line}`
        ).join("\n");
        
        return {
          file_name: file_name,
          start_line: start_line,
          end_line: actualEndLine,
          line_count: selectedLines.length,
          content_with_line_numbers: numberedContent,
        };
      } catch (e) {
        return { error: `Failed to read file range: ${e instanceof Error ? e.message : String(e)}` };
      }
    },
  });
tools.push(readFileRangeTool);

const searchInFileTool = tool({
    name: "search_in_file",
    description: catalog.search_in_file.description,
    parameters: {
      file_name: z.string(),
      pattern: z.string().describe("Search pattern (substring or regex)"),
      case_sensitive: z.boolean().optional().default(false).describe("Whether the search is case-sensitive (default: false)"),
      use_regex: z.boolean().optional().default(false).describe("Whether to treat pattern as a regex (default: false, treats as literal substring)"),
    },
    implementation: async ({ file_name, pattern, case_sensitive = false, use_regex = false }) => {
      try {
        const filePath = validatePath(ctx.cwd, file_name);
        const content = await readFile(filePath, "utf-8");
        const lines = content.split("\n");
        
        let matches: Array<{ line_number: number; content: string }> = [];
        
        for (let i = 0; i < lines.length; i++) {
          let line = lines[i];
          let searchPattern = pattern;
          
          if (!case_sensitive) {
            line = line.toLowerCase();
            searchPattern = pattern.toLowerCase();
          }
          
          let isMatch = false;
          if (use_regex) {
            try {
              const regex = new RegExp(searchPattern);
              isMatch = regex.test(line);
            } catch (e) {
              return { error: `Invalid regex pattern: ${e instanceof Error ? e.message : String(e)}` };
            }
          } else {
            isMatch = line.includes(searchPattern);
          }
          
          if (isMatch) {
            matches.push({
              line_number: i + 1,
              content: lines[i],
            });
          }
        }
        
        return {
          file_name: file_name,
          pattern: pattern,
          match_count: matches.length,
          matches: matches.slice(0, 100),
          note: matches.length > 100 ? `Showing first 100 of ${matches.length} matches` : undefined,
        };
      } catch (e) {
        return { error: `Failed to search file: ${e instanceof Error ? e.message : String(e)}` };
      }
    },
  });
tools.push(searchInFileTool);

const deleteLinesInFileTool = tool({
    name: "delete_lines_in_file",
    description: catalog.delete_lines_in_file.description,
    parameters: {
      file_name: z.string(),
      start_line: z.number().int().min(1).describe("The starting line number to delete (1-indexed)"),
      end_line: z.number().int().min(1).optional().describe("Optional: The ending line number to delete (inclusive). If omitted, only deletes start_line."),
    },
    implementation: async ({ file_name, start_line, end_line }) => {
      try {
        const filePath = validatePath(ctx.cwd, file_name);
        let content = "";
        try {
          content = await readFile(filePath, "utf-8");
        } catch {
          return { error: `File '${file_name}' does not exist.` };
        }

        const lines = content.split("\n");
        const actualEndLine = end_line ?? start_line;

        if (start_line > lines.length) {
          return { error: `Start line ${start_line} is beyond the end of the file (${lines.length} lines)` };
        }

        const deleteCount = Math.min(actualEndLine - start_line + 1, lines.length - start_line + 1);
        
        if (deleteCount <= 0) {
          return { error: `Invalid line range. End line must be >= Start line.` };
        }

        lines.splice(start_line - 1, deleteCount);

        await writeFile(filePath, lines.join("\n"), "utf-8");
        return { 
          success: true, 
          message: `Deleted ${deleteCount} line(s) (lines ${start_line}-${actualEndLine}) from ${file_name}`,
          new_line_count: lines.length 
        };
      } catch (e) {
        return { error: `Failed to delete lines: ${e instanceof Error ? e.message : String(e)}` };
      }
    },
  });
tools.push(deleteLinesInFileTool);
return tools;
}

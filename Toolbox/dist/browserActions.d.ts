export type BrowserAction = {
    type: "wait_for_selector";
    selector?: string;
} | {
    type: "wait";
    milliseconds?: number;
} | {
    type: "click";
    selector?: string;
} | {
    type: "type";
    selector?: string;
    text?: string;
} | {
    type: "press";
    key?: string;
} | {
    type: "select";
    selector?: string;
    value?: string;
} | {
    type: "hover";
    selector?: string;
} | {
    type: "scroll";
    selector?: string;
    x?: number;
    y?: number;
} | {
    type: "evaluate";
    script?: string;
};
export type BrowserLikePage = {
    waitForSelector(selector: string, options?: {
        timeout?: number;
    }): Promise<unknown>;
    click(selector: string, options?: {
        clickCount?: number;
    }): Promise<unknown>;
    type(selector: string, text: string, options?: {
        delay?: number;
    }): Promise<unknown>;
    select(selector: string, ...values: string[]): Promise<string[]>;
    hover(selector: string): Promise<unknown>;
    keyboard: {
        press(key: string): Promise<unknown>;
    };
    evaluate<T>(pageFunction: (...args: any[]) => T | Promise<T>, ...args: any[]): Promise<T>;
};
export declare function executeBrowserActions(page: BrowserLikePage, actions: BrowserAction[]): Promise<string[]>;
//# sourceMappingURL=browserActions.d.ts.map
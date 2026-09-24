"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findLMStudioHome = findLMStudioHome;
const fs_1 = require("fs");
const os_1 = require("os");
const path_1 = require("path");
let lmstudioHome = null;
function findLMStudioHome() {
    if (lmstudioHome !== null) {
        return lmstudioHome;
    }
    // if applicable, convert relative path to absolute and follow the symlink
    const resolvedHomeDir = (0, fs_1.realpathSync)((0, os_1.homedir)());
    const pointerFilePath = (0, path_1.join)(resolvedHomeDir, ".lmstudio-home-pointer");
    if ((0, fs_1.existsSync)(pointerFilePath)) {
        lmstudioHome = (0, fs_1.readFileSync)(pointerFilePath, "utf-8").trim();
        return lmstudioHome;
    }
    // See if ~/.cache/lm-studio exists. If it does, use it.
    const cacheHome = (0, path_1.join)(resolvedHomeDir, ".cache", "lm-studio");
    if ((0, fs_1.existsSync)(cacheHome)) {
        lmstudioHome = cacheHome;
        (0, fs_1.writeFileSync)(pointerFilePath, lmstudioHome, "utf-8");
        return lmstudioHome;
    }
    // Otherwise, fallback to ~/.lmstudio
    const home = (0, path_1.join)(resolvedHomeDir, ".lmstudio");
    lmstudioHome = home;
    (0, fs_1.writeFileSync)(pointerFilePath, lmstudioHome, "utf-8");
    return lmstudioHome;
}
//# sourceMappingURL=findLMStudioHome.js.map
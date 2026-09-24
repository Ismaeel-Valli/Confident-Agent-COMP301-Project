"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.IMPORT_DISTRIBUTIONS = void 0;
exports.queryPypi = queryPypi;
exports.verifyInterface = verifyInterface;
const verificationTypes_1 = require("./verificationTypes");
// Only explicit mappings are used. A PyPI project is not proof of an import path.
exports.IMPORT_DISTRIBUTIONS = { requests: 'requests', numpy: 'numpy', pandas: 'pandas', PIL: 'Pillow', sklearn: 'scikit-learn', yaml: 'PyYAML', bs4: 'beautifulsoup4', cv2: 'opencv-python' };
async function queryPypi({ library_name }, fetcher = fetch) {
    const top = library_name.split('.')[0], distribution = exports.IMPORT_DISTRIBUTIONS[top] || top;
    const source_url = `https://pypi.org/pypi/${encodeURIComponent(distribution)}/json`;
    const base = { source_url, retrieved_at: new Date().toISOString(), import_name: top, distribution };
    if (!/^[A-Za-z_][A-Za-z0-9_.-]*$/.test(top))
        return { ...base, exists: null, status: 'unverifiable', summary: 'Invalid or relative import name.' };
    try {
        const response = await fetcher(source_url, { signal: AbortSignal.timeout(8000) });
        if (response.status === 404)
            return { ...base, exists: false, status: 'not_found', summary: 'Distribution absent from PyPI; this alone does not prove an import nonexistent.' };
        if (!response.ok)
            return { ...base, exists: null, status: 'unverifiable', summary: `PyPI HTTP ${response.status}` };
        const data = await response.json();
        if (!data.info || typeof data.info.name !== 'string' || typeof data.info.version !== 'string')
            throw new Error('Malformed PyPI metadata');
        const normalize = (name) => name.toLowerCase().replace(/[-_.]+/g, '-');
        if (normalize(data.info.name) !== normalize(distribution))
            throw new Error('PyPI metadata names a different distribution.');
        return { ...base, exists: true, status: 'found', latest_version: data.info.version, summary: data.info.summary || '' };
    }
    catch (e) {
        return { ...base, exists: null, status: 'unverifiable', summary: `Package lookup failed: ${String(e)}` };
    }
}
async function verifyInterface({ claims, pypi_data = {} }) {
    const rows = (0, verificationTypes_1.ofType)(claims, 'import').map(imp => {
        const top = String(imp.library || '').split('.')[0];
        if (imp.stdlib === true)
            return (0, verificationTypes_1.result)('interface', 'verified_correct', 'tier_4', 'Python standard library inventory', `${top} is in this interpreter's standard library.`);
        if (imp.local)
            return (0, verificationTypes_1.unknown)('interface', `Local import ${imp.library} cannot be verified without its source.`);
        const datum = pypi_data[top];
        if (!datum || datum.status === 'unverifiable' || datum.exists === null)
            return (0, verificationTypes_1.unknown)('interface', `No usable package evidence for ${top}: ${datum?.summary || 'lookup missing'}`);
        // Unknown import-to-distribution mappings (including legitimate private modules) stay unknown.
        if (!Object.hasOwn(exports.IMPORT_DISTRIBUTIONS, top))
            return (0, verificationTypes_1.unknown)('interface', `No reviewed import-to-distribution mapping for ${top}; registry existence or 404 cannot settle this import.`);
        if (datum.status === 'not_found' && datum.exists === false)
            return (0, verificationTypes_1.unknown)('interface', `Expected distribution ${exports.IMPORT_DISTRIBUTIONS[top]} not found; cannot establish import nonexistence.`);
        if (datum.status !== 'found' || datum.exists !== true || datum.distribution !== exports.IMPORT_DISTRIBUTIONS[top])
            return (0, verificationTypes_1.unknown)('interface', `Inconsistent package evidence for ${top}: expected status=found, exists=true and distribution=${exports.IMPORT_DISTRIBUTIONS[top]}; received status=${datum.status}, exists=${datum.exists}, distribution=${datum.distribution ?? '(missing)'}. Preserve the full query_pypi result or use verify_candidate.`);
        return (0, verificationTypes_1.result)('interface', 'verified_correct', 'tier_2', 'PyPI metadata + reviewed import mapping', `${top} maps to ${datum.distribution} (${datum.latest_version || 'version unknown'}). Installation/callables checked separately by Pyright.`);
    });
    return (0, verificationTypes_1.aggregateExtracted)('interface', claims, rows, 'No imports in the extracted candidate.');
}
//# sourceMappingURL=packageEvidence.js.map
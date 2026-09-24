import { Claim, LayerResult, ofType, result, unknown, aggregateExtracted } from './verificationTypes';
export interface PackageEvidence { exists: boolean | null; status: 'found' | 'not_found' | 'unverifiable'; latest_version?: string; summary?: string; source_url?: string; retrieved_at?: string; import_name?: string; distribution?: string; }
// Only explicit mappings are used. A PyPI project is not proof of an import path.
export const IMPORT_DISTRIBUTIONS: Record<string,string> = {requests:'requests', numpy:'numpy', pandas:'pandas', PIL:'Pillow', sklearn:'scikit-learn', yaml:'PyYAML', bs4:'beautifulsoup4', cv2:'opencv-python'};
export async function queryPypi({library_name}:{library_name:string}, fetcher:typeof fetch = fetch): Promise<PackageEvidence> {
  const top = library_name.split('.')[0], distribution = IMPORT_DISTRIBUTIONS[top] || top;
  const source_url = `https://pypi.org/pypi/${encodeURIComponent(distribution)}/json`;
  const base = {source_url,retrieved_at:new Date().toISOString(),import_name:top,distribution};
  if (!/^[A-Za-z_][A-Za-z0-9_.-]*$/.test(top)) return {...base,exists:null,status:'unverifiable',summary:'Invalid or relative import name.'};
  try {
    const response = await fetcher(source_url,{signal:AbortSignal.timeout(8000)});
    if (response.status === 404) return {...base,exists:false,status:'not_found',summary:'Distribution absent from PyPI; this alone does not prove an import nonexistent.'};
    if (!response.ok) return {...base,exists:null,status:'unverifiable',summary:`PyPI HTTP ${response.status}`};
    const data:any = await response.json();
    if (!data.info || typeof data.info.name !== 'string' || typeof data.info.version !== 'string') throw new Error('Malformed PyPI metadata');
    const normalize = (name:string) => name.toLowerCase().replace(/[-_.]+/g,'-');
    if (normalize(data.info.name)!==normalize(distribution)) throw new Error('PyPI metadata names a different distribution.');
    return {...base,exists:true,status:'found',latest_version:data.info.version,summary:data.info.summary || ''};
  } catch(e) { return {...base,exists:null,status:'unverifiable',summary:`Package lookup failed: ${String(e)}`}; }
}
export async function verifyInterface({claims,pypi_data = {}}:{claims:Claim[];pypi_data?:Record<string,PackageEvidence>}): Promise<LayerResult> {
  const rows = ofType(claims,'import').map(imp => {
    const top = String(imp.library || '').split('.')[0];
    if (imp.stdlib === true) return result('interface','verified_correct','tier_4','Python standard library inventory',`${top} is in this interpreter's standard library.`);
    if (imp.local) return unknown('interface',`Local import ${imp.library} cannot be verified without its source.`);
    const datum = pypi_data[top];
    if (!datum || datum.status === 'unverifiable' || datum.exists === null) return unknown('interface',`No usable package evidence for ${top}: ${datum?.summary || 'lookup missing'}`);
    // Unknown import-to-distribution mappings (including legitimate private modules) stay unknown.
    if (!Object.hasOwn(IMPORT_DISTRIBUTIONS, top)) return unknown('interface',`No reviewed import-to-distribution mapping for ${top}; registry existence or 404 cannot settle this import.`);
    if (datum.status === 'not_found' && datum.exists === false) return unknown('interface',`Expected distribution ${IMPORT_DISTRIBUTIONS[top]} not found; cannot establish import nonexistence.`);
    if (datum.status !== 'found' || datum.exists !== true || datum.distribution !== IMPORT_DISTRIBUTIONS[top]) return unknown('interface',`Inconsistent package evidence for ${top}.`);
    return result('interface','verified_correct','tier_2','PyPI metadata + reviewed import mapping',`${top} maps to ${datum.distribution} (${datum.latest_version || 'version unknown'}). Installation/callables checked separately by Pyright.`);
  });
  return aggregateExtracted('interface',claims,rows,'No imports in the extracted candidate.');
}

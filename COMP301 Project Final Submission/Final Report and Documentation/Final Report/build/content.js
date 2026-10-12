// Assembles the report content from its parts (see build_report.js for the block types).
module.exports = {
  meta: { title: 'Static Verification of REST API Hallucinations in LLM-Generated Python Code', subtitle: 'COMP301 Confident Agent final report, The Skeptics, UKZN 2026' },
  blocks: [...require('./content_part1.js'), ...require('./content_part2.js'), ...require('./content_part3.js'), ...require('./content_part4.js')],
};

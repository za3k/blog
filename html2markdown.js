var TurndownService = require('turndown')
const fs = require("fs");

// Preview options at https://mixmark-io.github.io/turndown/
var turndownService = new TurndownService({
    linkStyle: 'referenced',
    hr: '---',
    headingStyle: 'atx',
    emDelimiter: '*',
    linkReferenceStyle: 'full',
    bulletListMarker: '-',
})

const html = fs.readFileSync(0, "utf-8");
const markdown = turndownService.turndown(html)
process.stdout.write(markdown);
process.stdout.write('\n');


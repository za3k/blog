var TurndownService = require('turndown')
var turndownPluginGfm = require('joplin-turndown-plugin-gfm')
const fs = require("fs")

function repeat (character, count) {
  return Array(count + 1).join(character)
}

var myPlugin = {
    pre: function(turndownService) {
      turndownService.addRule('preNoCode', {
        filter: function (node, options) {
          return (node.nodeName === 'PRE' && !node.firstElementChild)
        },

        replacement: function (content, node, options) {
          var code = node.textContent
          var fence = "```"
          var language = ''

          return (
            '\n\n' + fence + language + '\n' +
            code.replace(/\n$/, '') +
            '\n' + fence + '\n\n'
          )
        },
      })
    },

    preserveHTMLMatching: function(turndownService) {

    },
}


// Preview options at https://mixmark-io.github.io/turndown/
var turndownService = new TurndownService({
  linkStyle: 'inlined',
  hr: '---',
  headingStyle: 'atx',
  emDelimiter: '*',
  linkReferenceStyle: 'full',
  bulletListMarker: '-',
  codeBlockStyle: 'fenced',
})
turndownService.use(turndownPluginGfm.tables)
turndownService.use(myPlugin.pre)
turndownService.keep('iframe')
//turndownService.use(myPlugin.preserveHTMLMatching)

const html = fs.readFileSync(0, "utf-8");
const markdown = turndownService.turndown(html)
process.stdout.write(markdown);
process.stdout.write('\n');

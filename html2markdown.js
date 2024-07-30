var TurndownService = require('turndown')
var turndownPluginGfm = require('joplin-turndown-plugin-gfm')
const fs = require("fs")

function repeat (character, count) {
  return Array(count + 1).join(character)
}

function cleanAttribute (attribute) {
  return attribute ? attribute.replace(/(\n+\s*)+/g, '\n') : ''
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

    imageCaptions: function(turndownService) {
      turndownService.addRule('altTextIsFigCaption', {
        filter: 'img',
        replacement: function (content, node) {
          var alt = cleanAttribute(node.getAttribute('alt'))
          if (alt) alt = "alt:" + alt
          var title = cleanAttribute(node.getAttribute('title'))
          var titlePart = title ? ' "' + title + '"' : ''
          var src = node.getAttribute('src') || ''

          // Look for associated figcaption
          var figure = node
          while (figure && figure.nodeName != 'FIGURE') figure = figure.parentElement
          if (figure) {
            for (const child of Array.from(figure.children)) {
              if (child.nodeName == "FIGCAPTION") {
                alt = "caption:" + child.textContent
              }
              child.remove()
            }
          }

          return src ? '![' + alt + ']' + '(' + src + titlePart + ')' : ''
        }
      })
    }
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
turndownService.use(myPlugin.imageCaptions)
turndownService.keep('iframe')
turndownService.keep('video')
turndownService.preserve(function(node, options) {
    return node.nodeName == "FIGURE" && node.classList.contains("wp-block-gallery")
})

const html = fs.readFileSync(0, "utf-8");
const markdown = turndownService.turndown(html)
process.stdout.write(markdown);
process.stdout.write('\n');

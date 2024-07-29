const puppeteer = require('puppeteer')
const path = require('path')
const arguments = process.argv
const util = require('util');
const exec = util.promisify(require('child_process').exec);

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time))
}

async function compare(url1, url2, save1, save2, diff) {
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    const options = {
        fullPage: true,
        optimizeForSpeed: true,
    }

    await page.goto(`file://${path.join(__dirname, url1)}`)
    options.path = save1
    const render1 = await page.screenshot(options)

    await page.goto(`file://${path.join(__dirname, url2)}`)
    options.path = save2
    const render2 = await page.screenshot(options)


    const command = `compare -compose src ${save1} ${save2} ${diff}`
    try {
        await exec(command)
    } catch(err) {
        if (err.code !== 1) throw err
    }

    const result = await exec(`magick ${diff} -alpha off -fill black +opaque "#cccccc" \\( +clone -evaluate set 0 \\) -metric AE -compare -format "%[distortion] %w %h\n" info:`)

    const [pixelsSame, width, height] = result.stdout.trim().split(" ")

    const identical = !render1.compare(render2)
    const pixelsDifferent = height*width - pixelsSame
    heightDifference = Math.abs(render1.length - render2.length)
    var ret = {
      identical,
      heightDifference,
      pixelsDifferent,
      percentDifferent: pixelsDifferent / (pixelsDifferent + pixelsSame),
      rowsDifferent: pixelsDifferent / width,
      pixelsSame,
      height,
      width,
    }
    return ret
}

(async () => {
var ret = await compare(process.argv[2], process.argv[3], process.argv[4], process.argv[5], process.argv[6]);

process.stdout.write(JSON.stringify(ret))
process.stdout.write("\n")

if (!ret.identical) process.exitCode = 1
process.exit()
})();

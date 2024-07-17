const puppeteer = require('puppeteer')
const path = require('path')
const arguments = process.argv

async function compare(url1, url2) {
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    const options = {
        fullPage: true,
    }

    await page.goto(`file://${path.join(__dirname, url1)}`)
    const render1 = await page.screenshot(options)

    await page.goto(`file://${path.join(__dirname, url2)}`)
    const render2 = await page.screenshot(options)

    return !render1.compare(render2)
}

(async () => {
var same = await compare(process.argv[2], process.argv[3]);
if (same) process.exit(0)
else process.exit(1)
})();

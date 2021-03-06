const { spawn } = require('child_process')

const schema = require('./schema')

const pkgData = require('./package.json')

module.exports = function (app) {
  let child
 return {
    start: options => {
      let arguments = ['SK_x728bat.py']
      child = spawn('python3', arguments, { cwd: __dirname })

      child.stdout.on('data', data => {
	try {
        console.log(`"${data}"`)
        console.log(JSON.stringify(JSON.parse(data), null, 2))
        // app.debug(data.toString())
          app.handleMessage(undefined, JSON.parse(data.toString()))
        } catch (e) {
          console.error(e.message)
        }
      })

      child.stderr.on('data', fromChild => {
        console.error(fromChild.toString())
      })

      child.on('error', err => {
        console.error(err)
      })

      child.stdin.write(JSON.stringify(options))
      child.stdin.write('\n')
    },
    stop: () => {
      if (child) {
        process.kill(child.pid)
        child = undefined
      }
    },
    schema,
    id: pkgData.name,
    name: pkgData.description
  }
}
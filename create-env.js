const fs = require('fs')
const path = `./.env`
const vars = `
 REACT_APP_PUBLIC_KEY=${process.env.REACT_APP_PUBLIC_KEY}\n
 REACT_APP_TEMPLATE_ID=${process.env.REACT_APP_TEMPLATE_ID}\n
 REACT_APP_SERVICE_ID=${process.env.REACT_APP_SERVICE_ID}
`
fs.writeFileSync(path, vars)
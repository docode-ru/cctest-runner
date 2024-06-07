#!/usr/bin/env node
const fs = require('fs');

const stdin = process.openStdin();
stdin.addListener("data", function(input) {
  const stdInData = input.toString().trim().split('\n');
  const file = process.argv.slice(2)[0];

  if (file) {
    let code = fs.readFileSync(file, {encoding:'utf8', flag:'r'});
    let next = 0;
    code += `\nfunction prompt() { return stdInData[next++]; }`
    eval(code);
  }
});
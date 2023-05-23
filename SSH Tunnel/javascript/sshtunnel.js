/*
 * IPWorks SSH 2022 JavaScript Edition - Demo Application
 *
 * Copyright (c) 2023 /n software inc. - All rights reserved. - www.nsoftware.com
 *
 */
 
const readline = require("readline");
const ipworksssh = require("@nsoftware/ipworksssh");

if(!ipworksssh) {
  console.error("Cannot find ipworksssh.");
  process.exit(1);
}
let rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

main();

async function main() {
  const sshtunnel = new ipworksssh.sshtunnel();

  sshtunnel.on("Connected", (e) => (console.log(`Connection ${e.connectionId} Connected - ${e.description}`)))
  .on("Disconnected", (e) => (console.log(`Connection ${e.connectionId} Disconnected - ${e.description}`)))
  .on("SSHServerAuthentication", (e) => (e.accept = true))
  .on("ConnectionRequest", (e) => (console.log(`Connection request from ${e.address}: ${String(e.port)}`)))
  .on("Error", (e) => (console.log(e.description)));
  
  if (process.argv.length === 2) {
    // print help/usage
    console.log(
      "Usage:\n\tnode .\\sshtunnel.js <localport> <user@sshserver.com> <sshpassword> <sshforwardhost> <sshforwardport>"
    );
    process.exit(1);
  }

  sshtunnel.setLocalPort(parseInt(process.argv[2]));
  const sshinfo = process.argv[3].split("@");
  sshtunnel.setSSHHost(sshinfo[1]);
  sshtunnel.setSSHPort(22);
  sshtunnel.setSSHUser(sshinfo[0]);
  sshtunnel.setSSHPassword(process.argv[4]);
  sshtunnel.setSSHForwardHost(process.argv[5]);
  sshtunnel.setSSHForwardPort(parseInt(process.argv[6]));

  console.log("Starting SSH Tunnel ...");
  try {
    await sshtunnel.startListening();
  } catch (err) {
    console.log(err);
    process.exit(1);
  }
  console.log(`Listening on local port ${String(sshtunnel.getLocalPort())} ...`);
}


function prompt(promptName, label, punctuation, defaultVal)
{
  lastPrompt = promptName;
  lastDefault = defaultVal;
  process.stdout.write(`${label} [${defaultVal}] ${punctuation} `);
}
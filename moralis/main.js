const serverURL = '';
const appId = '';
Moralis.start({ serverURL, appId });

async function login() {
    let user = Moralis.User.current();
    if (!user) {
        try {
            user = await Moralis.authenticate({ signingMessage: "Authenticate" });
            console.log(user);
            console.log(user.get('ethAddress'));
        } catch(error) {
            console.log(error);
        }
    }
}

async function logOut() {
    await Moralis.User.logOut();
    console.log("Logged out");
}

document.getElementById("btn-login").onclick = login;
document.getElementById("btn-logout").onclick = logOut;
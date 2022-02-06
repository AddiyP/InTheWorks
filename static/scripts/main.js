window.onload = () => {
    console.log(userID);
    if (userID === 0)
    {
        return;
    }
    sessionStorage.setItem("userID", userID);
}

window.onload = () => {
    var form = document.querySelector("form");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        userId = sessionStorage.getItem("userID");
        console.log(userId);
        if (userId == 0) {
            console.log("Submit failed: not logged in");
        }
        else {
            form.creatorId.value = userId;
            form.submit();
        }
    });
}
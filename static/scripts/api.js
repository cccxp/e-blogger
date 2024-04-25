const api = axios.create({
    baseURL: "http://localhost:8000/api/v1"
})

api.interceptors.response.use((resp) => {
    return resp
}, (error) => {
    // unified error handling
    console.log(error)
    alert(error)
    return Promise.reject(error)
})

function checkLogin() {
    // Check the login status, if not logged in, redirect to the login page.
    // use this function in every page **EXCEPT** Login and Register page. 
    let token = localStorage.getItem("token")
    if (token) {
        api.get("/account/profile/me", {
            headers: {
                Authorization: "Bearer " + token
            }
        }).then(function (resp) {
            console.log(resp.data)
            if (resp.success) {
                // do nothing
            } else {
                // clear token data
                localStorage.clear()
                alert("please login first. ")
                window.location.href = "/static/Login.html";
            }
        })
    } else {
        alert("please login first. ")
        window.location.href = "/static/Login.html";
    }
}

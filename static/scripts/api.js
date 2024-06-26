const api = axios.create({
    baseURL: "http://207.148.69.162:10989/api/v1"  // for front-end integration use
    // baseURL: "http://localhost:8000/api/v1"  // for debug use
    // baseURL: "/api/v1"  // for production use
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
            if (resp.data.success) {
                // do nothing
            } else {
                // clear token data
                localStorage.clear()
                alert("please login first. ")
                window.location.href = "Login.html";
            }
        })
    } else {
        alert("please login first. ")
        window.location.href = "Login.html";
    }
}

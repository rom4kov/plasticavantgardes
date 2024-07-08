const likeButton = document.querySelector("#like-button")
const heart = document.querySelector("#heart");
const likeCount = document.getElementById('like-count');
const postId = likeButton.dataset.postId;
likeButton.addEventListener("click", () => {
    if (likeButton.dataset.userAuthenticated === 'true') {
        fetch(`/like-post/${postId}`, {
            method: "POST"
        })
            .then(response => response.json())
            .then(data => {
            let user_ids = [];
            for (const user of data.new_value) {
                user_ids.push(user.id);
            }
            if (data.new_value.length === 0) {
                likeCount.innerText = "";
                heart.style.fill = "none"
            } else if (data.new_value.length > 0 && !user_ids.includes(data.user_id)) {
                likeCount.innerText = data.new_value.length;
                heart.style.fill = "none"
            } else {
                likeCount.innerText = data.new_value.length;
                heart.style.fill = "currentColor"
            }
        })
            .catch(error => {
            console.error('Error:', error);
        });
    } else {
        console.log("Please log in or register to like posts.")
        fetch("/like-post/{{ post.id }}", {
            method: "POST",
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
            if (response.status === 401) {
                return response.json().then(data => {
                    if (data.redirect) {
                        // Store the flash message in session storage
                        sessionStorage.setItem('flashMessage', data.message);
                        // Redirect the browser to the login page
                        window.location.href = data.redirect;
                    }
                });
            } else if (response.redirected) {
                console.log(response)
                window.location.href = data.redirect;
            } else {
                return response.text();
            }
        })
            .then(data => {
            if (data) {
                // Handle the data returned from the server if not redirected
                console.log(data);
            }
        })
    }
})

const commentLikeButtons = document.querySelectorAll("#comment-like-button")
for (const btn of commentLikeButtons) {
    const commentId = btn.dataset.commentId;
    const commentHeart = btn.children[0].children[0];
    const commentLikeCount = btn.children[1];
    btn.addEventListener("click", () => {
        if (btn.dataset.userAuthenticated === 'True') {
            fetch(`/like-comment/${commentId}`, {
                method: "POST"
            })
                .then(response => response.json())
                .then(data => {
                let user_ids = [];
                for (const user of data.new_value) {
                    user_ids.push(user.id);
                }
                if (data.new_value.length === 0) {
                    commentLikeCount.innerText = "";
                    commentHeart.style.fill = "none"
                } else if (data.new_value.length > 0 && !user_ids.includes(data.user_id)) {
                    commentLikeCount.innerText = data.new_value.length;
                    commentHeart.style.fill = "none"
                } else {
                    commentLikeCount.innerText = data.new_value.length;
                    commentHeart.style.fill = "currentColor"
                }
            })
                .catch(error => {
                console.error('Error:', error);
            });
        } else {
            fetch(`/like-comment/${commentId}`, {
                method: "POST",
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => {
                if (response.status === 401) {
                    return response.json().then(data => {
                        if (data.redirect) {
                            // Store the flash message in session storage
                            sessionStorage.setItem('flashMessage', data.message);
                            // Redirect the browser to the login page
                            window.location.href = data.redirect;
                        }
                    });
                } else if (response.redirected) {
                    console.log(response)
                    window.location.href = data.redirect;
                } else {
                    return response.text();
                }
            })
                .then(data => {
                if (data) {
                    // Handle the data returned from the server if not redirected
                    console.log(data);
                }
            })
        }
    })
}

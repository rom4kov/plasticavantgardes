const replyButtons = document.querySelectorAll("#reply-btn");
for (const btn of replyButtons) {
    btn.addEventListener("click", () => {
        const comment_id = btn.dataset.commentId;
        const replies = document.querySelector(`#replies-${comment_id}`);
        if (replies.classList.contains("hidden")) {
            replies.classList.remove("hidden");
        } else {
            replies.classList.add("hidden");
        }
    })
}

function replyToComment(comment_id) {
    const replyText = document.querySelector(`#textarea-${comment_id}`).value;
    const replies = document.querySelector(`#replies-inner-${comment_id}`);

    fetch(`/reply-to-comment/${comment_id}`, {
        method: "POST",
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: replyText
        })
    })

    const repliesCount = document.querySelector("#replies-count");
    repliesCount.innerText = parseInt(repliesCount.innerText) + 1;
    const newReply = document.querySelector("#template-reply");
    newReply.children[1].children[1].innerText = replyText;
    replies.appendChild(newReply);
    newReply.classList.remove("hidden");
    const replyTextarea = document.querySelector(`#textarea-${comment_id}`);
    replyTextarea.value = "";
}

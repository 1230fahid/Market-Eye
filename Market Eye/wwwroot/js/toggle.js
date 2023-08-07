function toggle(btn) {
    if (btn.type === "password") {
        btn.type = "text";
    } else {
        btn.type = "password";
    }
}
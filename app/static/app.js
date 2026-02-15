const socket = io("/ws");
socket.on("message", data=>{
  const d=document.createElement("div");
  d.textContent=data;
  document.getElementById("chat").appendChild(d);
});
function send(){
  const v=document.getElementById("msg").value;
  socket.emit("message", v);
}

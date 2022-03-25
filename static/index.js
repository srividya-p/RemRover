var socket = io(document.domain + ':' + location.port, { reconnection:false });
var messageButton = document.getElementById('server_message');
    
socket.on('connect', function() {
	socket.emit('connected', {data: 'I\'m connected!'});
});

//SERVO CONTROLS
document.getElementById('p_l').addEventListener("click", function(){ 
	socket.emit('pan_left'); 
});

document.getElementById('p_r').addEventListener("click", function(){ 
	socket.emit('pan_right');
});

document.getElementById('t_u').addEventListener("click", function(){ 
	socket.emit('tilt_up'); 
});

document.getElementById('t_d').addEventListener("click", function(){ 
	socket.emit('tilt_down'); 
});

//MOVEMENT CONTROLS
document.getElementById('m_f').addEventListener("mousedown", function(){ 
	socket.emit('move_forward'); 
});

document.getElementById('m_f').addEventListener("mouseup", function(){ 
	socket.emit('stop_movement'); 
});

document.getElementById('m_b').addEventListener("mousedown", function(){ 
	socket.emit('move_backward'); 
});

document.getElementById('m_b').addEventListener("mouseup", function(){ 
	socket.emit('stop_movement'); 
});

document.getElementById('m_l').addEventListener("mousedown", function(){ 
	socket.emit('move_left'); 
});

document.getElementById('m_l').addEventListener("mouseup", function(){ 
	socket.emit('stop_movement'); 
});

document.getElementById('m_r').addEventListener("mousedown", function(){ 
	socket.emit('move_right'); 
});

document.getElementById('m_r').addEventListener("mouseup", function(){ 
	socket.emit('stop_movement'); 
});


var orignalMessage = 'Messages from server will be displayed here.'

socket.on('t_u_limit', function(message) {
	messageButton.innerText = message
	
	setTimeout(function() { 
		messageButton.innerText = orignalMessage 
	}, 2000);
})

socket.on('t_d_limit', function(message) {
	messageButton.innerText = message
	
	setTimeout(function() { 
		messageButton.innerText = orignalMessage 
	}, 2000);
})

socket.on('p_l_limit', function(message) {
	messageButton.innerText = message
	
	setTimeout(function() { 
		messageButton.innerText = orignalMessage 
	}, 2000);
})

socket.on('p_r_limit', function(message) {
	messageButton.innerText = message
	
	setTimeout(function() { 
		messageButton.innerText = orignalMessage 
	}, 2000);
})




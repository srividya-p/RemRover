var socket = io(document.domain + ':' + location.port, { reconnection:false });
var messageButton = document.getElementById('server_message');
    
socket.on('connect', function() {
	socket.emit('connected', {data: 'I\'m connected!'});
});


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




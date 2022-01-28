var socket = io(document.domain + ':' + location.port, { reconnection:false });
    
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




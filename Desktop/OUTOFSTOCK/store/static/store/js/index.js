// home page - floating shape follows mouse slightly

document.addEventListener('DOMContentLoaded', function() {
    var shape = document.querySelector('.floating-shape');
    if (!shape) return;

    window.addEventListener('mousemove', function(e) {
        var x = (e.clientX / window.innerWidth - 0.5) * 18;
        var y = (e.clientY / window.innerHeight - 0.5) * 18;
        shape.style.transform = 'rotate(16deg) translate(' + x + 'px, ' + y + 'px)';
    });
});

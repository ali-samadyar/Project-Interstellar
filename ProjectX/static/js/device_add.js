function openAddDeviceModal() {
    document.getElementById('addDeviceModal').style.display = 'block';
}

// Close the modal
function closeAddDeviceModal() {
    document.getElementById('addDeviceModal').style.display = 'none';
}

// Close the modal if the user clicks outside of it
window.onclick = function (event) {
    var modal = document.getElementById('addDeviceModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
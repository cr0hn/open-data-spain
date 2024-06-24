function initializeDeleteButtons() {
    const deleteButtons = document.querySelectorAll('.delete-confirmation');

    deleteButtons.forEach(button => {
        // Get title from property of "button" element
        const title = button.getAttribute('data-popup-title') || 'Esta seguro?';

        // Get text from property of "button" element
        const text = button.getAttribute('data-popup-text') || "No podrá revertir esta acción!";

        // Get confirm button text from property of "button" element
        const confirmButtonText = button.getAttribute('data-popup-confirm-button-text') || 'Borrar!';


        button.addEventListener('click', (event) => {
            event.preventDefault();

            Swal.fire({
                title: title,
                text: text,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: confirmButtonText
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = button.href;
                }
            })
        });
    });
}

const registrationEndModalElement = document.getElementById('registrationEndModal')
const registrationEndModal = new bootstrap.Modal(registrationEndModalElement, {})

const registrationEndModalToggle = () => {
    registrationEndModal.toggle()
}

document.addEventListener("DOMContentLoaded", function (event) {
    const queryString = window.location.search
    const urlParams = new URLSearchParams(queryString)
    const isRegistrationEnd = urlParams.get('registration')
    if (isRegistrationEnd) {
        registrationEndModalToggle()
    }
})
function renderDriverTab() {
    let target = document.querySelector('.parking__tab.driver')
    target.style.display = 'none'
    let another = document.querySelector('.parking__tab.owner')
    another.style.display = 'flex'
}

function renderOwnerTab() {
    let another = document.querySelector('.parking__tab.driver')
    another.style.display = 'none'
    let target = document.querySelector('.parking__tab.owner')
    target.style.display = 'flex'

}

function proveEditing() {
    let modal = document.querySelector('.modal')
    modal.style.display = 'block'
    modal.innerHTML = `
      <div id="editing-modal" class="modal__body">
    <div class="modal__header">
      <h2 class="modal__title">Нужен пароль</h2>
      <button
          type="button"
          onclick="toggleModal()"
          class="modal__close"
      >
      </button>
    </div>
    <div class="modal__main">
       <h5 class="modal__text">
        Подтвердите что вы — владелец аккаунта, чтобы сменить сведения в профиле
      </h5>
      <label class="modal__label">
        Пароль
      </label>
      <div class="modal__input-container">
        <input
            id="password"
            type="password"
            class="modal__input"
            placeholder="*********"
        >
        <button
            onclick="togglePassword()"
            class="modal__hide-password">
          <img src="static/icons/eye-off.svg" alt="">
        </button>
      </div>
      <button
        style="align-self: flex-end; margin-bottom: 0"
        class="modal__submit"
        onclick="confirmEditing()"
    >
      Продолжить
    </button>
    </div>
    
  </div>
    `
}
function confirmEditing() {

}
function setActiveProfileTab() {
    if (event.target.innerText === 'Водитель' && !event.target.classList.contains('active')) {
        document.querySelector('.parking__tabs-button.active').classList.remove('active')
        event.target.classList.add('active')
        renderDriverTab()
    }
    if (event.target.innerText === 'Владелец' && !event.target.classList.contains('active')) {
        document.querySelector('.parking__tabs-button.active').classList.remove('active')
        event.target.classList.add('active')
        renderOwnerTab()
    }
}
describe('R8: Test todolist', () => {
    let uid // user id
    let name // user name
    let email // user email
  
    before('create a user', () => {
        cy.fixture('user.json').then((user) => {
            cy.request({
                method: 'POST',
                url: "localhost:5000/users/create",
                form: true,
                body: user
            }).then((response) => {
                uid = response.body._id.$oid
                name = user.firstName + ' ' + user.lastName
                email = user.email
            })
        })
    })

    before('create a task', () => {
        cy.fixture('task.json').then((task) => {
            task.userid = uid
            cy.request({
                method: 'POST',
                url: "localhost:5000/tasks/create",
                form: true,
                body: task
            })
        })
    })

    beforeEach(function () {
        cy.visit('localhost:3000')
        cy.get('.inputwrapper #email').type('mon.doe@gmail.com')
        cy.get('form').submit()
        cy.get('.container-element').eq(0).find('a').click()
    })

    describe('R8UC1', () => {
        it('create a new todo item with description', () => {
            cy.viewport(1000, 800)

            cy.get('.inline-form')
            .find('input[type=text]')
            .type('Download video')

            cy.get('.inline-form')
            .find('input[type=submit]')
            .click()

            cy.get('.todo-item').eq(0)
            .should('contain.text', 'Download video')
        })

        it('add button is disabled with empty description', () => {
            cy.get('.inline-form')
            .find('input[type=submit]')
            .should('be.disabled');
        })
    })

    describe('R8UC2', () => {
        it('toggle a todo item to mark it as done', () => {
            cy.viewport(1000, 1000)

            cy.get('li.todo-item').first()
            .find('span.checker')
            .click()
            
            cy.get('li.todo-item').first()
            .find('span.checker')
            .then($checker => {
                expect($checker).to.have.css('text-decoration')
            })
        })
    })

    describe('R8UC3', () => {
        it('todo item to be deleted when x symbol is clicked', () => {
            cy.get('.todo-item').eq(0)
            .find('span.remover')
            .click()

            cy.get('.todo-list')
            .should('not.have.class', 'todo-item')
            .and('have.length', 1)
        })
    })

    after(function () {
        cy.request({
            method: 'DELETE',
            url: `localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})

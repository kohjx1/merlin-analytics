/**
 * @jest-environment jsdom
 */

import '@testing-library/jest-dom'
import { render } from '@testing-library/svelte'
// import Home from '../+page.svelte'

describe('home', () => {
    const GUEST_USER = {
        username: 'guest',
        groups: ["merlin-admin"]
        // groups: []
    }
    const FAKE_USER: User = {
        username: 'test',
        groups: ['test-group1', 'test-group2']
    }
    test('welcome message', () => {
    //     const home = render(Home)
    //     const welcome = home.getByText('Welcome to Merlin')
        // expect(welcome).toBeInTheDocument()
    })
    // test('welcome username', () => {
    //     const home = render(Home, { data: { user: GUEST_USER } })
    //     const welcome = home.getByText('Welcome to Merlin, guest')
    //     expect(welcome).toBeInTheDocument()
    // })
    // test('welcome list groups', () => {
    //     const home = render(Home, { data: { user: FAKE_USER } })
    //     const welcome = home.getByText('Welcome to Merlin, test')
    //     expect(welcome).toBeInTheDocument()
    //     const groups = home.getByText('You are part of the following groups:')
    //     expect(groups).toBeInTheDocument()
    //     const test_group = home.getByText('test-group1')
    //     expect(test_group).toBeInTheDocument()
    // })
})

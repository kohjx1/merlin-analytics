import type { RequestEvent, Cookies } from '@sveltejs/kit';
import { createMock } from 'ts-auto-mock';
import { UnsecuredJWT, type JWTPayload } from 'jose';
import { injectCredentials } from '../functions/auth';

class mockGetterSetter {
    private _headers: Record<string, string> = {};
    get(name: string): string | null {
        return this._headers[name];
    }
    set(name: string, value: string): void {
        this._headers[name] = value;
    }
}

describe('auth', () => {
    // guest user
    const GUEST_USER = {
        username: 'guest',
        groups: ["merlin-admin"]
        // groups: []
    }
    // fake user
    const FAKE_USER = {
        username: 'test',
        groups: ['test']
    }
    // id token for fake user
    const payload: JWTPayload = {
        preferred_username: FAKE_USER.username,
        groups: FAKE_USER.groups
    }
    const jwt = new UnsecuredJWT(payload).encode()
    test('guest user without cookies or headers', () => {
        let event = createMock<RequestEvent>();
        injectCredentials(event)
        expect(event.locals.user).toEqual(GUEST_USER)
    })
    test('retrieve id token from cookie', () => {
        const mock = new mockGetterSetter()
        mock.set('id.token', jwt)
        const cookies: unknown = mock
        let event = createMock<RequestEvent>({ cookies: cookies as Cookies })
        injectCredentials(event)
        expect(event.locals.user).toEqual(FAKE_USER)
    })
    test('retrieve id token from header', () => {
        const mock = new mockGetterSetter()
        mock.set('X-Id-Token', jwt)
        const headers: unknown = mock
        const request = createMock<Request>({ headers: headers as Headers })
        let event = createMock<RequestEvent>({ request });
        injectCredentials(event)
        expect(event.locals.user).toEqual(FAKE_USER)
    })
})

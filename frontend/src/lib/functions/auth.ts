import type { RequestEvent } from '@sveltejs/kit';
import * as jose from 'jose';

// default credentials as guest and group-less
const GUEST_USER: User = {
    username: "guest",
    // groups: []
    groups: ["merlin-admin"]
    // groups: ["merlin-user"]
}

/**
 * Function to inject user credentials into event locals
 * @param {RequestEvent} event
 */
export const injectCredentials = (event: RequestEvent) => {
    const idToken = getIdToken(event);
    const user = createUser(idToken);
    event.locals.user = user;
}

/**
 * Function to extract id token from incoming request
 * @param {RequestEvent} event
 */
const getIdToken = (event: RequestEvent): string | null => {
    // get id token from cookie
    let idToken = event.cookies.get('id.token');

    // get from header if id token expired
    if (!idToken && event.request && event.request.headers) {
        const idTokenHeader = event.request.headers.get('X-Id-Token');
        // check if id token exists
        // may not exist if running locally without forwardauth
        if (idTokenHeader) {
            // strip Bearer prefix
            idToken = idTokenHeader.slice(7);
            event.cookies.set('id.token', idToken);
        }
    }

    // return id token if found
    // null if not in cookie or header
    return idToken ? idToken : null
}

/**
 * Function to create user from id token
 * @param {string | null} idToken
 */
const createUser = (idToken: string | null): User => {
    let user: User = GUEST_USER;

    // decode id token for user info and groups
    if (idToken) {
        const decoded = jose.decodeJwt(idToken);
        const username = decoded.preferred_username;
        if (typeof username === "string") {
            user.username = username;
        }
        const groups = decoded.groups
        if (Array.isArray(groups) &&
            groups.every(element => typeof element === "string")) {
            user.groups = groups;
        };
    }

    return user;
}

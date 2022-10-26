import type { Handle } from '@sveltejs/kit';
import { injectCredentials } from './lib/functions/auth';

// sets the username and groups
export const handle: Handle = async ({ event, resolve }) => {
    // inject user credentials to event locals
    injectCredentials(event);
    return resolve(event);
};

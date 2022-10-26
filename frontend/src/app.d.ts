/// <reference types="@sveltejs/kit" />
/// <reference types="unplugin-icons/types/svelte" />

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
// and what to do when importing types
interface User {
	username: string
	groups: Array<string>
}

declare namespace App {
	interface Locals {
		user: User
	}
	// interface PageData {}
	// interface Platform {}
}

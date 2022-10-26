<script>
  /** @type {import('./$types').PageData} */

  export let data;
  const user = data.user;
  console.log(user);

  import ManagementPortal from './managementPortal/+page.svelte'
  import UserPortal from './userPortal/+page.svelte'
</script>

{#if user}
  {#if user.groups}
    <!-- <p>You are part of the following groups:</p> -->
    <ul>
      {#each user.groups as group}
        <!-- <li>{group}</li> -->
      {/each}
    </ul>
	{#if user.groups.includes("merlin-admin")}
		<ManagementPortal user={user}/>
	{:else}
		<UserPortal user={user}/>
	{/if}
  {/if}
{:else}
  <h1>Welcome to Merlin</h1>
{/if}
<!-- {#if user}
  <h1>Welcome to Merlin, {user.username}</h1>
  {#if user.groups}
    <p>You are part of the following groups:</p>
    <ul>
      {#each user.groups as group}
        <li>{group}</li>
      {/each}
    </ul>
  {/if}
{:else}
  <h1>Welcome to Merlin</h1>
{/if} -->

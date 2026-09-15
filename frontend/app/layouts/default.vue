<script setup>
const navItems = [
    { label: 'Home', to: '/' },
    { label: 'Movies', to: '/movies' },
    { label: 'Tickets', to: '/tickets' }
]
</script>

<template>
<div class="mx-auto flex min-h-screen max-w-md flex-col bg-surface">
    <main class="flex-1 px-4 pb-20 pt-4">
        <NuxtPage />
    </main>
    <AppTabBar :items="navItems" />
</div>
</template>
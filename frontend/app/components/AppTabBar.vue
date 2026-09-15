<script setup lang="ts">
interface NavItem {
  label: string
  to: string
}

defineProps<{ items: NavItem[] }>()
</script>

<template>
  <nav class="fixed inset-x-0 bottom-4 z-10 mx-auto flex w-full max-w-md justify-around rounded-2xl border border-zinc-200 bg-white/90 px-2 py-2 shadow-lg backdrop-blur">
    <NuxtLink
      v-for="item in items"
      :key="item.to"
      :to="item.to"
      class="flex-1 rounded-xl py-2 text-center text-sm font-medium text-zinc-500 transition hover:bg-brand-soft hover:text-brand"
    >
      {{ item.label }}
    </NuxtLink>
  </nav>
</template>
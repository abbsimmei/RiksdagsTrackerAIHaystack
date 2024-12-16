<template>
    <div>
        <NuxtLayout>
            <NuxtPage />
        </NuxtLayout>
    </div>
</template>


<script setup lang="ts">

//Documentation: https://nuxt.com/docs/getting-started/seo-meta
useHead({
    title: 'RiksdagsTracker',
    meta: [
        { name: 'RiksdagsTracker', content: 'My amazing site.' }
    ],
    bodyAttrs: {
        class: 'test'
    },
    script: [{}]
})
</script>
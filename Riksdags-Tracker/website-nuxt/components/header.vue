<template>
  <!-- Navbar container -->
  <nav class="flex items-center justify-between px-4 py-2 bg-[#2f074e] text-white border-b-2 border-white">

    <!-- Logo aligned to the left -->
    <div class="flex-shrink-0">
      <NuxtLink to="/">
        <NuxtImg src="/icons/small-Riksdags-Tracker-loggo.png" alt="Logo" class="h-12" />
      </NuxtLink>
    </div>

    <!-- Navigation links aligned to the right -->
    <div class="flex-grow text-right space-x-6">
      <NuxtLink to="/" class="text-sm hover:text-gray-400">Home</NuxtLink>
      <NuxtLink to="/ledamoter" class="text-sm hover:text-gray-400">Ledamöter</NuxtLink>
      <NuxtLink to="/partier" class="text-sm hover:text-gray-400">Partier</NuxtLink>
      <NuxtLink to="/skriftligaFragor" class="text-sm hover:text-gray-400">Skriftliga Frågor</NuxtLink>
      <NuxtLink to="/" class="text-sm hover:text-gray-400">WIP (about us)</NuxtLink>
      <NuxtLink to="/AI" class="text-sm hover:text-gray-400">WIP (AI)</NuxtLink>
    </div>

  </nav>
</template>

<script setup lang="js">

</script>

<style scoped></style>
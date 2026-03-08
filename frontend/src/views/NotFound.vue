<template>
  <div class="min-h-[60vh] flex items-center justify-center">
    <div class="card p-12 text-center space-y-6 max-w-lg">
      <div class="space-y-4">
        <h1 class="text-6xl font-extrabold text-gray-200">404</h1>
        <h2 class="text-3xl font-bold text-gray-900">Page Not Found</h2>
        <p class="text-gray-600 leading-relaxed">
          The page you are looking for doesn't exist or has been moved.
        </p>
      </div>

      <router-link
        to="/"
        class="btn btn-primary inline-flex items-center gap-2"
      >
        <span>←</span>
        Back to Home
      </router-link>
    </div>
  </div>
</template>

<template>
  <div class="py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto text-center">
      <h1 class="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl mb-6">
        Simple Leave Management
      </h1>
      <p class="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
        Apply for leaves, track your request status, and manage team availability in one simple place. Built for speed and clarity.
      </p>

      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
        <template v-if="!authStore.isLoggedIn">
          <router-link to="/register" class="btn btn-primary">
            Create Account
          </router-link>
          <router-link to="/login" class="btn btn-secondary">
            Sign In
          </router-link>
        </template>
        <template v-else>
          <router-link
            :to="authStore.isEmployee ? '/employee/dashboard' : '/employer/dashboard'"
            class="btn btn-primary"
          >
            Go to Dashboard
          </router-link>
        </template>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 text-left">
        <div class="card">
          <h2 class="text-xl font-bold mb-3">For Employees</h2>
          <ul class="space-y-2 text-gray-600">
            <li class="flex items-center">
              <span class="text-blue-500 mr-2">✔</span> Apply for casual, sick, or annual leave
            </li>
            <li class="flex items-center">
              <span class="text-blue-500 mr-2">✔</span> Track request status in real-time
            </li>
            <li class="flex items-center">
              <span class="text-blue-500 mr-2">✔</span> View leave history and remarks
            </li>
          </ul>
        </div>

        <div class="card">
          <h2 class="text-xl font-bold mb-3">For Employers</h2>
          <ul class="space-y-2 text-gray-600">
            <li class="flex items-center">
              <span class="text-blue-500 mr-2">✔</span> Review all employee leave requests
            </li>
            <li class="flex items-center">
              <span class="text-blue-500 mr-2">✔</span> Approve or reject with one click
            </li>
            <li class="flex items-center">
              <span class="text-blue-500 mr-2">✔</span> Provide specific feedback/remarks
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
</script>

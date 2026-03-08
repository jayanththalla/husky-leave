<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">My Dashboard</h1>
        <p class="text-gray-600">Track and manage your leave requests</p>
      </div>
      <router-link to="/employee/apply-leave" class="btn btn-primary">
        Apply for Leave
      </router-link>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card border-l-4 border-l-yellow-400">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-yellow-50 text-yellow-600 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 uppercase">Pending</p>
            <p class="text-2xl font-bold text-gray-900">{{ leavesStore.pendingCount }}</p>
          </div>
        </div>
      </div>

      <div class="card border-l-4 border-l-green-400">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-50 text-green-600 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 uppercase">Approved</p>
            <p class="text-2xl font-bold text-gray-900">{{ leavesStore.approvedCount }}</p>
          </div>
        </div>
      </div>

      <div class="card border-l-4 border-l-red-400">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-red-50 text-red-600 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 uppercase">Rejected</p>
            <p class="text-2xl font-bold text-gray-900">{{ leavesStore.rejectedCount }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter and List -->
    <div class="card !p-0 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200 flex flex-col sm:flex-row justify-between items-center gap-4">
        <h2 class="text-lg font-bold text-gray-900">Leave Requests</h2>
        <div class="flex items-center space-x-2">
          <button
            v-for="status in ['pending', 'approved', 'rejected']"
            :key="status"
            @click="toggleFilter(status)"
            :class="[
              'px-3 py-1 rounded-md text-xs font-semibold uppercase tracking-wider transition-colors',
              leavesStore.filterStatus === status
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            {{ status }}
          </button>
          <button
            v-if="leavesStore.filterStatus"
            @click="leavesStore.clearFilter()"
            class="text-gray-400 hover:text-gray-600 p-1"
          >
            &times;
          </button>
        </div>
      </div>

      <div class="divide-y divide-gray-200">
        <div v-if="leavesStore.loading" class="p-12 text-center text-gray-500">
          Syncing your records...
        </div>

        <div v-else-if="leavesStore.filteredLeaves.length === 0" class="p-12 text-center text-gray-500 italic">
          No records found.
        </div>

        <div
          v-for="leave in leavesStore.filteredLeaves"
          :key="leave._id"
          class="px-6 py-6 hover:bg-gray-50 transition-colors"
        >
          <div class="flex flex-col md:flex-row justify-between items-start gap-4">
            <div class="space-y-2 flex-grow">
              <div class="flex items-center gap-2">
                <span class="font-bold text-gray-900 capitalize">{{ leave.leave_type }} Leave</span>
                <span
                  :class="[
                    'px-2 py-0.5 rounded text-[10px] uppercase font-bold',
                    leave.status === 'approved' ? 'bg-green-100 text-green-700' :
                    leave.status === 'rejected' ? 'bg-red-100 text-red-700' :
                    'bg-yellow-100 text-yellow-700'
                  ]"
                >
                  {{ leave.status }}
                </span>
              </div>
              
              <div class="flex items-center gap-4 text-sm text-gray-500">
                <span class="flex items-center gap-1">
                  📅 {{ leave.start_date }} to {{ leave.end_date }}
                </span>
                <span class="flex items-center gap-1">
                  ⏱ {{ leave.number_of_days }} Days
                </span>
              </div>

              <p class="text-gray-600 text-sm italic border-l-2 border-gray-100 pl-3">
                "{{ leave.reason }}"
              </p>
              
              <div v-if="leave.remarks" class="mt-3 p-3 bg-blue-50 text-blue-800 text-sm rounded-md border border-blue-100">
                <span class="font-bold block text-xs uppercase text-blue-600 mb-1">Employer Remarks</span>
                {{ leave.remarks }}
              </div>
            </div>
            
            <div class="text-right shrink-0">
              <span class="text-[10px] text-gray-400 uppercase tracking-widest block">
                #{{ leave._id.slice(-6) }}
              </span>
              <span class="text-[10px] text-gray-400 block mt-1">
                {{ new Date(leave.created_at).toLocaleDateString() }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useLeavesStore } from '@/stores/leavesStore'

const leavesStore = useLeavesStore()

onMounted(async () => {
  await leavesStore.fetchMyLeaves()
})

function toggleFilter(status) {
  if (leavesStore.filterStatus === status) {
    leavesStore.clearFilter()
  } else {
    leavesStore.setFilter(status)
  }
}
</script>

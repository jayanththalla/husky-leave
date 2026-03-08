<template>
  <div class="space-y-8">
    <!-- Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900">Admin Portal</h1>
      <p class="text-gray-600">Review and manage team leave requests</p>
    </div>

    <!-- Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card border-l-4 border-l-yellow-400">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-yellow-50 text-yellow-600 mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 uppercase">Pending Review</p>
            <p class="text-2xl font-bold text-gray-900">{{ totalPending }}</p>
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
            <p class="text-sm font-medium text-gray-500 uppercase">Approved Total</p>
            <p class="text-2xl font-bold text-gray-900">{{ totalApproved }}</p>
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
            <p class="text-sm font-medium text-gray-500 uppercase">Rejected Total</p>
            <p class="text-2xl font-bold text-gray-900">{{ totalRejected }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Requests Management -->
    <div class="card !p-0 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200 flex flex-col sm:flex-row justify-between items-center gap-4 bg-gray-50">
        <h2 class="text-lg font-bold text-gray-900">Manage Requests</h2>
        <div class="flex items-center space-x-1">
          <button
            v-for="status in ['pending', 'approved', 'rejected', null]"
            :key="status"
            @click="loadByStatus(status)"
            :class="[
              'px-3 py-1 rounded-md text-[10px] font-bold uppercase tracking-widest transition-all',
              currentStatus === status
                ? 'bg-blue-600 text-white shadow-sm'
                : 'bg-white border border-gray-300 text-gray-600 hover:bg-gray-50'
            ]"
          >
            {{ status || 'all' }}
          </button>
        </div>
      </div>

      <div class="divide-y divide-gray-200 min-h-[300px]">
        <div v-if="leavesStore.loading" class="p-12 text-center text-gray-500">
          Fetching requests...
        </div>

        <div v-else-if="leavesStore.leaves.length === 0" class="p-12 text-center text-gray-500 italic">
          No requests to show.
        </div>

        <div
          v-for="leave in leavesStore.leaves"
          :key="leave._id"
          class="px-6 py-6 hover:bg-gray-50 transition-colors"
        >
          <div class="flex flex-col lg:flex-row gap-6">
            <!-- Employee Column -->
            <div class="lg:w-1/4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-700 font-bold flex items-center justify-center">
                  {{ leave.employee_name.charAt(0) }}
                </div>
                <div>
                  <h3 class="font-bold text-gray-900">{{ leave.employee_name }}</h3>
                  <p class="text-[10px] text-gray-500 uppercase tracking-tighter">ID: {{ leave.employee_id || leave._id.slice(-6) }}</p>
                </div>
              </div>
              <div class="mt-2">
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
            </div>

            <!-- Detail Column -->
            <div class="lg:w-2/4 space-y-3">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <span class="text-[10px] uppercase font-bold text-gray-400 block">Category</span>
                  <p class="font-semibold text-gray-800 capitalize">{{ leave.leave_type }}</p>
                </div>
                <div>
                  <span class="text-[10px] uppercase font-bold text-gray-400 block">Duration</span>
                  <p class="font-semibold text-gray-800">{{ leave.number_of_days }} Days</p>
                </div>
              </div>
              
              <div>
                <span class="text-[10px] uppercase font-bold text-gray-400 block">Reason</span>
                <p class="text-sm text-gray-600 italic mt-1 border-l-2 border-gray-100 pl-3">"{{ leave.reason }}"</p>
              </div>

              <div v-if="leave.remarks" class="p-3 bg-gray-50 rounded border border-gray-100 text-sm">
                <span class="font-bold block text-[10px] uppercase text-gray-500 mb-1">Decision Remarks</span>
                <p class="text-gray-700">{{ leave.remarks }}</p>
              </div>
            </div>

            <!-- Action Column -->
            <div class="lg:w-1/4 lg:text-right">
              <div v-if="leave.status === 'pending'" class="space-y-3 lg:ml-auto max-w-sm">
                <textarea
                  v-model="remarks[leave._id]"
                  rows="2"
                  class="input-field text-xs resize-none"
                  placeholder="Decision remarks..."
                ></textarea>
                <div class="flex gap-2">
                  <button
                    @click="handleApprove(leave._id)"
                    :disabled="leavesStore.loading"
                    class="flex-1 py-1.5 bg-green-600 text-white rounded text-xs font-bold uppercase hover:bg-green-700 disabled:opacity-50"
                  >
                    Approve
                  </button>
                  <button
                    @click="handleReject(leave._id)"
                    :disabled="leavesStore.loading"
                    class="flex-1 py-1.5 bg-red-600 text-white rounded text-xs font-bold uppercase hover:bg-red-700 disabled:opacity-50"
                  >
                    Reject
                  </button>
                </div>
              </div>
              <div v-else>
                <p class="text-[10px] text-gray-400 uppercase font-bold mb-1">Processed</p>
                <p class="text-xs text-gray-600">{{ new Date(leave.updated_at || leave.created_at).toLocaleDateString() }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref, computed } from 'vue'
import { useLeavesStore } from '@/stores/leavesStore'

const leavesStore = useLeavesStore()
const currentStatus = ref(null)
const remarks = ref({})

const totalPending = computed(() => leavesStore.leaves.filter((l) => l.status === 'pending').length)
const totalApproved = computed(() => leavesStore.leaves.filter((l) => l.status === 'approved').length)
const totalRejected = computed(() => leavesStore.leaves.filter((l) => l.status === 'rejected').length)

onMounted(async () => {
  await leavesStore.fetchAllLeaves()
})

async function loadByStatus(status) {
  currentStatus.value = status
  await leavesStore.fetchAllLeaves(status)
}

async function handleApprove(leaveId) {
  const remark = remarks.value[leaveId] || ''
  try {
    await leavesStore.updateLeaveStatus(leaveId, 'approved', remark)
    delete remarks.value[leaveId]
  } catch (error) {
    // Error is handled by leavesStore
  }
}

async function handleReject(leaveId) {
  const remark = remarks.value[leaveId] || ''
  if (!remark) {
    alert('Please provide remarks for rejection')
    return
  }
  try {
    await leavesStore.updateLeaveStatus(leaveId, 'rejected', remark)
    delete remarks.value[leaveId]
  } catch (error) {
    // Error is handled by leavesStore
  }
}
</script>

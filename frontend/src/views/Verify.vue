<template>
  <div class="max-w-xl mx-auto mt-20 p-6 border rounded shadow bg-white">
    <h2 class="text-2xl font-bold mb-4 text-center">Reservation Verification</h2>
    <p class="mb-4 text-justify">Please enter the 6-digit code sent to your email to verify your reservation. A <strong>confirmation message</strong> will be sent to the email you registered.</p>

    <input
      v-model="code"
      maxlength="6"
      class="w-full p-2 border mb-4"
      placeholder="Enter verification code"
    />

    <button
      @click="verify"
      class="cursor-pointer w-full bg-green-800 text-white py-2 rounded hover:bg-green-700"
    >
      Verify Reservation
    </button>

    <p v-if="verified" class="mt-4 text-center text-green-600 font-semibold">Reservation verified successfully! Please check your email.</p>
    <p v-if="error" class="mt-4 text-red-600">{{ error }}</p>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useToast } from 'vue-toastification'

  const route = useRoute()
  const router = useRouter()
  const toast = useToast()

  const token = ref(route.query.token || '')
  const code = ref('')
  const verified = ref(false)
  const error = ref('')
  let loadingId = null

  onMounted(() => {
    if (!token.value) {
      toast.warning("No reservation token found. Redirecting...")
      setTimeout(() => router.push('/'), 2000)
    }
  })

  const verify = async () => {
    error.value = ''
    if (!token.value || !code.value) {
      error.value = "Missing token or code."
      toast.error("Missing token or code.")
      return
    }

    loadingId = toast.info("Verifying reservation...", { timeout: false })

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_BASE_URL
      const res = await fetch(`${backendUrl}/reserve/verify_reservation/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reservation_token: token.value, code: code.value })
      })

      const result = await res.json()
      toast.dismiss(loadingId)

      if (res.ok && result.success) {
        verified.value = true
        toast.success("Reservation verified successfully! Please check your email.")
        setTimeout(() => router.push('/'), 3000)
      } else {
        error.value = result.error || "Verification failed"
        toast.error(error.value)
      }
    } catch (err) {
      toast.dismiss(loadingId)
      error.value = "Network error: " + err.message
      toast.error(error.value)
    }
  }
</script>
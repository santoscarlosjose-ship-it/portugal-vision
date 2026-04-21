import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

// Este código corre nos servidores do Supabase (Edge Functions)
serve(async (req) => {
  try {
    // Recebe os dados do pedido que mudou na base de dados
    const { record } = await req.json()

    // 1. SEGURANÇA: Só dispara o WhatsApp se o estado for 'pronto'
    if (record.estado !== 'pronto') {
      return new Response(JSON.stringify({ message: "Ignorado: Estado não é pronto" }), { status: 200 })
    }

    // 2. DADOS: Pega no telefone e nome que estão na tabela 'pedidos'
    const telefone = record.telefone; 
    const nome = record.nome_cliente || "Cliente";

    if (!telefone) {
      return new Response(JSON.stringify({ error: "Pedido sem número de telefone" }), { status: 400 })
    }

    // 3. CONFIGURAÇÃO: Estas chaves tu vais configurar no painel do Supabase depois
    const WHATSAPP_TOKEN = Deno.env.get("WHATSAPP_TOKEN")
    const PHONE_NUMBER_ID = Deno.env.get("WHATSAPP_PHONE_ID")

    // 4. MENSAGEM: O que o cliente vai receber
    const payload = {
      messaging_product: "whatsapp",
      to: telefone, // O número deve ter o prefixo (ex: 351910000000)
      type: "text",
      text: { 
        body: `Olá ${nome}! Boas notícias da Portugal Vision: o seu pedido já está pronto e à sua espera! 🍳` 
      }
    }

    // 5. ENVIO: Fala com a API do WhatsApp (Meta)
    const response = await fetch(`https://graph.facebook.com/v17.0/${PHONE_NUMBER_ID}/messages`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${WHATSAPP_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    const result = await response.json()

    return new Response(JSON.stringify({ success: true, result }), {
      headers: { "Content-Type": "application/json" },
      status: 200,
    })

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { status: 500 })
  }
})

def notificacao_desktop(em_processo: list) -> None:
    # tratar multiplas entradas de execução em uma só notification
    mensagem_detalhes: str

    match len(em_processo):
        case 1: mensagem_detalhes = f"O programa {em_processo[0].args[3]} não está autorizado a abrir agora."
        case varios_apps: mensagem_detalhes = f"Os programas {em_processo} em questão não estão autorizados a abrir agora."

    toast("App Restrictor",
          mensagem_detalhes)


def notificar_finalizacao(apps: list):
    apenas_um_app = (len(apps) == 1)

    if apenas_um_app:
        processo = finalizar_execucao(apps[0])
        notificacao_desktop(em_processo=[execucao])

    else:
        execucoes = []

        for app in apps:
            processo = finalizar_execucao(app)
            execucoes.append(processo.returncode)
        
    
       notificacao_desktop(em_processo=execucoes)

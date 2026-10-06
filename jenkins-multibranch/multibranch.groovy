// Job DSL seed: one multibranch pipeline that discovers branches (PR discovery needs a SCM-provider source such as GitHub, not plain Git).
multibranchPipelineJob('orders') {
  displayName('Orders service')
  branchSources {
    branchSource {
      source {
        git {
          id('orders-git')
          remote('https://example.invalid/orders.git')
          traits {
            gitBranchDiscovery()
          }
        }
      }
      strategy {
        defaultBranchPropertyStrategy {
          props {
            noTriggerBranchProperty()
          }
        }
      }
    }
  }
  factory {
    workflowBranchProjectFactory {
      scriptPath('Jenkinsfile')
    }
  }
  orphanedItemStrategy {
    discardOldItems {
      numToKeep(10)
      daysToKeep(14)
    }
  }
  triggers {
    periodicFolderTrigger {
      interval('1d')
    }
  }
}

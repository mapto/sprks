from models.policies import policies_model


class TestPolicies:

    def test_policy_parser(self):
        model = policies_model()
        # result = model.generate_samples({'prenew': 3, 'pattempts': 3, 'pdict': 0, 'psets': 2, 'phist': 4})
        # result = model.generate_samples({'plen': 0})
        # result = model.generate_samples({})
        #model.generate_training_set()
        #policy = model.latest_policy(3)

        policyUpdate = [
        {
          'employee': ['executives', 'road'],
          'location': ['office', 'home'],
          'device': ['phone', 'desktop'],
          'policyDelta': {
               'pwpolicy': {'plen': 12,
                    'pdict': 1},
               'passfaces': {},
               'biometric': {}
          }
        },
        {
          'employee': ['desk', 'road'],
          'location': ['office', 'public'],
          'device': ['desktop', 'laptop'],
          'policyDelta': {
           'pwpolicy': {'plen': 8,
            'psets': 3},
           'passfaces': {},
           'biometric': {'bdata': 2}
          }
        },
            {
                'employee': ['desk'],
                'location':['office'],
                'device':['desktop'],
                'policyDelta': {
                   'pwpolicy': {'plen':0},
                   'passfaces': {'pdata': 1},
                    'biometric': {}
                }
            }]

        """ updated_policy = model.parse_policy(policyUpdate)
            latest_policy_before = model.iter_to_nested_obj(model.get_policy_history(4, True))
            latest_policy_after = model.merge_policies(updated_policy, latest_policy_before)
            print "updated_policy", updated_policy
            print "latest_policy before", model.nested_obj_to_list_of_dict(latest_policy_before)

            #print model.get_latest_policy(4)[1]

            print "latest_policy after", model.nested_obj_to_list_of_dict(latest_policy_after)"""
        #model.commit_policy_update(policyUpdate, '2014-02-15')
        #print model.nested_obj_to_list_of_dict(model.iter_to_nested_obj(model.get_policy_history(2)))
        #print model.get_policy_history(4)[0]
        #print model.get_policies_list(1)
        model.merge_policies(model.parse_policy(policyUpdate), model.iter_to_nested_obj(model.get_policy_history(2)))
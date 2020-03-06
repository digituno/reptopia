import factory
from faker import Factory

fake_ko = Factory.create('ko_KR')  # 한글 더미 데이터 생성기
fake_en = Factory.create()  # 영어 더미 데이터 생성기

class AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'account.Account'

    email = factory.sequence(lambda _ : fake_ko.email())
    password = factory.sequence(lambda _ : fake_ko.password())
    name = factory.sequence(lambda _ : fake_ko.name())
    bio = factory.sequence(lambda _ : fake_ko.text(max_nb_chars=200, ext_word_list=None))


class PetFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'pet.Pet'

    name = factory.sequence(lambda _ : fake_ko.job())
    person = factory.SubFactory(PersonFactory)

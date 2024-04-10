import graphene
from graphene_django import DjangoObjectType
from app.models import *


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        
class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryNode)

    def mutate(self, info, name):
        category = Category(name=name)
        category.save()
        return CreateCategory(category=category)

class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    category = graphene.Field(CategoryNode)

    def mutate(self, info, id, name):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        return UpdateCategory(category=category)

class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            category = Category.objects.get(pk=id)
            category.delete()
            success = True
        except Category.DoesNotExist:
            success = False
        return DeleteCategory(success=success)




class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        
class CreateIngredient(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        category_id = graphene.ID(required=True)

    ingredient = graphene.Field(IngredientNode)

    def mutate(self, info, name, notes, category_id):
        ingredient = Ingredient(name=name, notes=notes, category_id=category_id)
        ingredient.save()
        return CreateIngredient(ingredient=ingredient)

class UpdateIngredient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        notes = graphene.String()
        category_id = graphene.ID()

    ingredient = graphene.Field(IngredientNode)

    def mutate(self, info, id, name=None, notes=None, category_id=None):
        ingredient = Ingredient.objects.get(pk=id)
        if name is not None:
            ingredient.name = name
        if notes is not None:
            ingredient.notes = notes
        if category_id is not None:
            ingredient.category_id = category_id
        ingredient.save()
        return UpdateIngredient(ingredient=ingredient)

class DeleteIngredient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            ingredient = Ingredient.objects.get(pk=id)
            ingredient.delete()
            success = True
        except Ingredient.DoesNotExist:
            success = False
        return DeleteIngredient(success=success)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()
    delete_ingredient = DeleteIngredient.Field()




class Query(graphene.ObjectType):
    category = graphene.Field(CategoryNode, id=graphene.ID())
    categories = graphene.List(CategoryNode)

    ingredient = graphene.Field(IngredientNode, id=graphene.ID())
    ingredients = graphene.List(IngredientNode)


    def resolve_category(self, info, id):
        return Category.objects.get(pk=id)

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_ingredient(self, info, id):
        return Ingredient.objects.get(pk=id)

    def resolve_ingredients(self, info):
        return Ingredient.objects.all()


schema = graphene.Schema(query=Query, mutation=Mutation)



'''
Category


mutation create {
  createCategory(name: "Category4") {
    category {
      id
      name
    }
  }
}

mutation update {
  updateCategory(id: 2, name: "dairy") {
    category {
      id
      name
    }
  }
}

mutation delete {
  deleteCategory(id: 11) {
    success
  }
}
'''


'''
Ingredient
mutation create {
  createIngredient(name: "rice",
    notes: "good for health",
    categoryId: 5) {
    ingredient {
      id
      name
      notes
      category {
        id
        name
      }
    }
  }
}


mutation update{
  updateIngredient(id: 8,
    name: "wheat") {
    ingredient {
      id
      name
    }
  }
}


mutation delete {
  deleteIngredient(id: 1) {
    success
  }
}
'''
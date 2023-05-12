#define MAX_ITERATION 1000
int ERRORS_COUNT = 0;
void Generate_NAF()
{
    for (int i = 0; i < MAX_ITERATION; i++)
        for (int j = 0; j < MAX_ITERATION; j++)
            TAU_NAF(i, j);
}

void Generate_NAF_CC()
{
    for (int i = 0; i < MAX_ITERATION; i++)
        for (int j = 0; j < MAX_ITERATION; j++)
            TAU_NAF_CC(i, j);
}

void Generate_double_NAF()
{
    for (int i = 0; i < MAX_ITERATION; i++)
        for (int j = 0; j < MAX_ITERATION; j++)
            double_NAF(i, j);
}

void Generate_double_NAF_CC()
{
    for (int i = 0; i < MAX_ITERATION; i++)
        for (int j = 0; j < MAX_ITERATION; j++)
            double_NAF_CC(i, j);
}

void Generate_best_double_NAF_CC()
{
    for (int i = 0; i < MAX_ITERATION; i++)
        for (int j = 0; j < MAX_ITERATION; j++)
            best_double_NAF_CC(i, j);
}

bool cohrency_checker(int *result, int zero_counter, int size)
{
    int zero_counts = 0;
    for (int i = 0; i < size; i++)
    {
        if (result[i] == 0)
            zero_counts += 1;
    }
    if (zero_counter == zero_counts)
        return 1;
    else
        return 0;
}

bool best_cohrency_checker(int *result, int zero_counter,
                           int positive_counter, int negative_counter, int size)
{
    int zero_counts = 0;
    int positive_counts = 0;
    int negative_counts = 0;
    for (int i = 0; i < size; i++)
    {
        if (result[i] == 0)
            zero_counts += 1;
        else if(result[i] == 1)
            positive_counts += 1;
        else if(result[i] == -1)
            negative_counts += 1;
    }
    if (zero_counter != zero_counts)
        return 0;
    if (positive_counter != positive_counts)
        return 0;
    if (negative_counter != negative_counts)
        return 0;
    return 1;
}

int double_NAF(int d0, int d1)
{
    int meu = 1;
    int c0 = d0;
    int c1 = d1;
    int size = 0;
    int u0;
    int u1;
    int *result = (int *)malloc(sizeof(int));
    while (c0 != 0 || c1 != 0)
    {
        int temp = (c0 - 2 * c1) % 4; // changed in c code
        if (temp < 0)
        {
            temp = temp + 4;
        }
        int u = temp;

        if (u == 3)
        {
            u0 = -1;
            u1 = 0;
        }
        else if (u == 2)
        {
            u0 = 0;
            u1 = 1;
            int temp = ((2 * (((c1 % 4) + 1) % 4)) % 8);
            if ((temp % 8) == (c0 % 8))
            {
                u1 = -1;
            }
        }
        else if (u == 1)
        {
            u0 = 1;
            u1 = 0;
        }
        else
        {
            u0 = 0;
            u1 = 0;
        }

        c0 = c0 - u0;
        c1 = c1 - u1;
        result = (int *)realloc(result, (size + 2) * sizeof(int));
        result[size++] = u0;
        result[size++] = u1;
        int temp_c0 = c0;
        int temp_c1 = c1;
        c0 = ((-1 * temp_c0) + (2 * meu * temp_c1)) / 4;
        c1 = -1 * ((meu * temp_c0) + (2 * temp_c1)) / 4;
    }
    free(result);
}

int double_NAF_CC(int d0, int d1)
{
    int meu = 1;
    int c0 = d0;
    int c1 = d1;
    int size = 0;
    int u0;
    int u1;
    int zero_counter = 0;
    int *result = (int *)malloc(sizeof(int));
    while (c0 != 0 || c1 != 0)
    {
        int temp = (c0 - 2 * c1) % 4; // changed in c code
        if (temp < 0)
        {
            temp = temp + 4;
        }
        int u = temp;

        if (u == 3)
        {
            u0 = -1;
            u1 = 0;
            zero_counter += 1;
        }
        else if (u == 2)
        {
            u0 = 0;
            u1 = 1;
            int temp = ((2 * (((c1 % 4) + 1) % 4)) % 8);
            if ((temp % 8) == (c0 % 8))
            {
                u1 = -1;
            }
            zero_counter += 1;
        }
        else if (u == 1)
        {
            u0 = 1;
            u1 = 0;
            zero_counter += 1;
        }
        else
        {
            u0 = 0;
            u1 = 0;
            zero_counter += 2;
        }
        c0 = c0 - u0;
        c1 = c1 - u1;
        result = (int *)realloc(result, (size + 2) * sizeof(int));
        result[size++] = u0;
        result[size++] = u1;
        int temp_c0 = c0;
        int temp_c1 = c1;
        c0 = ((-1 * temp_c0) + (2 * meu * temp_c1)) / 4;
        c1 = -1 * ((meu * temp_c0) + (2 * temp_c1)) / 4;
    }

    if (cohrency_checker(result, zero_counter, size) == 0)
    {
        ERRORS_COUNT += 1;
    }
    free(result);
}



int best_double_NAF_CC(int d0, int d1)
{
    int meu = 1;
    int c0 = d0;
    int c1 = d1;
    int size = 0;
    int u0;
    int u1;
    int zero_counter = 0;
    int positive_counter = 0;
    int negative_counter = 0;
    int *result = (int *)malloc(sizeof(int));
    while (c0 != 0 || c1 != 0)
    {
        int temp = (c0 - 2 * c1) % 4; // changed in c code
        if (temp < 0)
        {
            temp = temp + 4;
        }
        int u = temp;

        if (u == 3)
        {
            u0 = -1;
            u1 = 0;
            zero_counter += 1;
            negative_counter += 1;
        }
        else if (u == 2)
        {
            u0 = 0;
            u1 = 1;
            int temp = ((2 * (((c1 % 4) + 1) % 4)) % 8);
            if ((temp % 8) == (c0 % 8))
            {
                u1 = -1;
                negative_counter += 1;
            }else{
                positive_counter += 1;
            }
            zero_counter += 1;
        }
        else if (u == 1)
        {
            u0 = 1;
            u1 = 0;
            zero_counter += 1;
            positive_counter += 1;
        }
        else
        {
            u0 = 0;
            u1 = 0;
            zero_counter += 2;
        }
        c0 = c0 - u0;
        c1 = c1 - u1;
        result = (int *)realloc(result, (size + 2) * sizeof(int));
        result[size++] = u0;
        result[size++] = u1;
        int temp_c0 = c0;
        int temp_c1 = c1;
        c0 = ((-1 * temp_c0) + (2 * meu * temp_c1)) / 4;
        c1 = -1 * ((meu * temp_c0) + (2 * temp_c1)) / 4;
    }

    if (best_cohrency_checker(result, zero_counter,positive_counter,negative_counter,size) == 0)
    {
        ERRORS_COUNT += 1;
    }
    free(result);
}

int TAU_NAF_CC(int d0, int d1)
{

    int meu = 1;
    int c0 = d0;
    int c1 = d1;
    int size = 0;
    int *result = (int *)malloc(sizeof(int));
    int zero_counter = 0;
    while (c0 != 0 || c1 != 0)
    {
        int output_bit;
        if (c0 % 2 != 0) // Changed in c code, -13%2 == -1 in c
        {
            int temp = (c0 - 2 * c1) % 4; // changed in c code
            if (temp < 0)
            {
                temp = temp + 4;
            }
            output_bit = 2 - temp;
            c0 = c0 - output_bit;
        }
        else
        {
            output_bit = 0;
            zero_counter += 1;
        }
        int temp_c0 = c0;
        int temp_c1 = c1;
        c0 = temp_c1 + (meu * temp_c0 / 2);
        c1 = -temp_c0 / 2;
        result = (int *)realloc(result, (size + 1) * sizeof(int));
        result[size++] = output_bit;
    }

    if (cohrency_checker(result, zero_counter, size) == 0)
    {
        ERRORS_COUNT += 1;
    }
    free(result);


    return 0;
}
int TAU_NAF(int d0, int d1)
{

    int meu = 1;
    int c0 = d0;
    int c1 = d1;
    int size = 0;
    int *result = (int *)malloc(sizeof(int));

    while (c0 != 0 || c1 != 0)
    {
        int output_bit;
        if (c0 % 2 != 0) // Changed in c code, -13%2 == -1 in c
        {
            int temp = (c0 - 2 * c1) % 4; // changed in c code
            if (temp < 0)
            {
                temp = temp + 4;
            }
            output_bit = 2 - temp;
            c0 = c0 - output_bit;
        }
        else
        {
            output_bit = 0;
        }
        int temp_c0 = c0;
        int temp_c1 = c1;
        c0 = temp_c1 + (meu * temp_c0 / 2);
        c1 = -temp_c0 / 2;
        result = (int *)realloc(result, (size + 1) * sizeof(int));
        result[size++] = output_bit;
    }
    free(result);
}